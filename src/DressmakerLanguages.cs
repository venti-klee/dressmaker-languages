using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using BepInEx;
using HarmonyLib;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace DressmakerLanguages {
    [BepInPlugin("local.dressmaker.languages", "Dressmaker Languages", "0.1.0")]
    [BepInDependency("yuu.dressmaker.mods")]
    public sealed class Plugin : BaseUnityPlugin {
        internal static Plugin Current;
        internal static bool Applying;
        readonly Dictionary<int, Tracked> tracked = new Dictionary<int, Tracked>();
        readonly HashSet<string> seen = new HashSet<string>(StringComparer.Ordinal);
        readonly HashSet<string> pending = new HashSet<string>(StringComparer.Ordinal);
        Dictionary<string, string> translations = new Dictionary<string, string>(StringComparer.Ordinal);
        HashSet<string> known = new HashSet<string>(StringComparer.Ordinal);
        readonly Dictionary<string, TMP_FontAsset> fonts = new Dictionary<string, TMP_FontAsset>();
        string directory, language = "zh-CN", fingerprint = "";
        float nextPoll;
        Harmony harmony;
        sealed class Tracked { public Component Component; public string Source, Rendered; }

        void Awake() {
            Current = this;
            directory = Path.Combine(Paths.ConfigPath, "DressmakerLanguages");
            Directory.CreateDirectory(directory);
            Reload();
            harmony = new Harmony("local.dressmaker.languages");
            int count = 0;
            var prefix = new HarmonyMethod(typeof(Plugin), "TextPrefix");
            var postfix = new HarmonyMethod(typeof(Plugin), "SetTextPostfix");
            foreach (Type type in new[] { typeof(TMP_Text), typeof(Text) }) {
                var setter = type.GetProperty("text").GetSetMethod();
                try { harmony.Patch(setter, prefix: prefix); count++; }
                catch (Exception e) { Logger.LogWarning("Could not patch " + type.Name + ": " + e.Message); }
            }
            foreach (var m in typeof(TMP_Text).GetMethods(BindingFlags.Public | BindingFlags.Instance)) {
                if (m.Name != "SetText" || m.GetParameters().Length == 0 || m.GetParameters()[0].ParameterType != typeof(string)) continue;
                try { harmony.Patch(m, postfix: postfix); count++; }
                catch (Exception e) { Logger.LogWarning("Could not patch SetText: " + e.Message); }
            }
            Logger.LogInfo("Dressmaker Languages ready; language=" + language + "; text hooks=" + count + "; translations=" + translations.Count);
        }
        static void TextPrefix(Component __instance, ref string value) {
            if (Applying || Current == null || String.IsNullOrEmpty(value)) return;
            try { value = Current.Resolve(__instance, value); }
            catch (Exception e) { Current.Logger.LogWarning("Text hook: " + e.Message); }
        }
        static void SetTextPostfix(TMP_Text __instance) {
            if (Applying || Current == null) return;
            try {
                string before = __instance.text;
                string after = Current.Resolve(__instance, before);
                if (before != after) { Applying = true; __instance.text = after; }
            } catch (Exception e) { Current.Logger.LogWarning("SetText hook: " + e.Message); }
            finally { Applying = false; }
        }
        bool FromLoader(Component component) {
            for (Transform t = component.transform; t != null; t = t.parent) {
                string n = t.name.ToLowerInvariant();
                if (n.Contains("modmanager") || n.Contains("mod manager") || n.Contains("modsettings") || n.Contains("fabriccreator") || n.Contains("accessorycreator")) return true;
            }
            var frames = new StackTrace(false).GetFrames();
            if (frames != null) foreach (var frame in frames) {
                var method = frame.GetMethod();
                if (method != null && method.DeclaringType != null && method.DeclaringType.Assembly.GetName().Name == "DressmakerMods") return true;
            }
            return false;
        }
        string Resolve(Component component, string source) {
            if (String.IsNullOrWhiteSpace(source) || source.Length > 2000 || !source.Any(c => (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z'))) return source;
            int id = component.GetInstanceID();
            Tracked previous;
            if (tracked.TryGetValue(id, out previous) && previous.Rendered == source) return source;
            if (!known.Contains(source) && !FromLoader(component)) {
                tracked.Remove(id); // The same pooled label can later hold a base-game item.
                return source;
            }
            string output;
            if (language == "en") output = source;
            else if (!translations.TryGetValue(source, out output) || String.IsNullOrEmpty(output)) {
                output = source;
                if (seen.Count < 20000 && seen.Add(source)) pending.Add(source);
            }
            tracked[id] = new Tracked { Component = component, Source = source, Rendered = output };
            if (source != output) EnsureFont(component, output);
            return output;
        }
        void EnsureFont(Component component, string text) {
            var tmp = component as TMP_Text;
            if (tmp == null || tmp.font == null || tmp.font.HasCharacters(text)) return;
            try {
                TMP_FontAsset asset;
                if (!fonts.TryGetValue(language, out asset)) {
                    string[] names = language == "ko" ? new[] { "Apple SD Gothic Neo", "Malgun Gothic", "Noto Sans CJK KR" } :
                        language == "ja" ? new[] { "Hiragino Sans", "Yu Gothic", "Noto Sans CJK JP" } :
                        new[] { "PingFang SC", "Microsoft YaHei", "Noto Sans CJK SC", "Arial Unicode MS" };
                    var available = new HashSet<string>(Font.GetOSInstalledFontNames());
                    string name = names.FirstOrDefault(n => available.Contains(n));
                    if (name == null) return;
                    var font = Font.CreateDynamicFontFromOSFont(name, 32);
                    asset = TMP_FontAsset.CreateFontAsset(font);
                    asset.name = "DressmakerLanguages-" + language;
                    DontDestroyOnLoad(asset);
                    fonts[language] = asset;
                }
                if (tmp.font.fallbackFontAssetTable == null) tmp.font.fallbackFontAssetTable = new List<TMP_FontAsset>();
                if (!tmp.font.fallbackFontAssetTable.Contains(asset)) tmp.font.fallbackFontAssetTable.Add(asset);
                asset.TryAddCharacters(text);
            } catch (Exception e) { Logger.LogWarning("Font fallback: " + e.Message); }
        }
        void Update() {
            if (Time.unscaledTime < nextPoll) return;
            nextPoll = Time.unscaledTime + 2f;
            try {
                if (pending.Count > 0) {
                    using (var writer = new StreamWriter(Path.Combine(directory, "pending.jsonl"), true, new UTF8Encoding(false)))
                        foreach (var text in pending) writer.WriteLine(JsonConvert.SerializeObject(new { source = text, kind = "display" }));
                    pending.Clear();
                }
                if (Reload()) Refresh();
                foreach (var item in tracked.Where(p => p.Value.Component == null).ToArray()) tracked.Remove(item.Key);
            } catch (Exception e) { Logger.LogWarning("Translation sync: " + e.Message); }
        }
        bool Reload() {
            string config = Path.Combine(directory, "runtime.json");
            if (!File.Exists(config)) return false;
            var j = JObject.Parse(File.ReadAllText(config));
            string target = (string)j["language"] ?? "zh-CN";
            if (!(new[] { "zh-CN", "ja", "ko", "fr", "de", "es", "en" }).Contains(target)) return false;
            string dictionary = Path.Combine(directory, "translations." + target + ".json");
            string sources = Path.Combine(directory, "known-sources.json");
            string stamp = target + "|" + File.GetLastWriteTimeUtc(config).Ticks + "|" + File.GetLastWriteTimeUtc(dictionary).Ticks + "|" + File.GetLastWriteTimeUtc(sources).Ticks;
            if (stamp == fingerprint) return false;
            var next = File.Exists(dictionary) ? JsonConvert.DeserializeObject<Dictionary<string, string>>(File.ReadAllText(dictionary)) : new Dictionary<string, string>();
            var keys = File.Exists(sources) ? JsonConvert.DeserializeObject<string[]>(File.ReadAllText(sources)) : new string[0];
            if (language != target) { seen.Clear(); pending.Clear(); }
            language = target;
            translations = next ?? new Dictionary<string, string>();
            known = new HashSet<string>(keys ?? new string[0], StringComparer.Ordinal);
            fingerprint = stamp;
            return true;
        }
        void Refresh() {
            Applying = true;
            try {
                foreach (var pair in tracked.ToArray()) {
                    var item = pair.Value;
                    if (item.Component == null) { tracked.Remove(pair.Key); continue; }
                    string value;
                    if (language == "en" || !translations.TryGetValue(item.Source, out value)) value = item.Source;
                    if (String.IsNullOrEmpty(value)) value = item.Source;
                    EnsureFont(item.Component, value);
                    var tmp = item.Component as TMP_Text;
                    var ui = item.Component as Text;
                    // Avoid overwriting a label repurposed by a pool or another plugin.
                    string current = tmp != null ? tmp.text : ui != null ? ui.text : null;
                    if (current != item.Rendered) { tracked.Remove(pair.Key); continue; }
                    if (tmp != null) tmp.text = value;
                    else if (ui != null) ui.text = value;
                    item.Rendered = value;
                }
            } finally { Applying = false; }
        }
        void OnDestroy() { if (harmony != null) harmony.UnpatchSelf(); Current = null; }
    }
}
