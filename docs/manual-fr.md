# Installation manuelle de Dressmaker Languages

Installez d'abord [Yuuma ModLoader pour Mac](https://www.nexusmods.com/dressmaker/mods/1?tab=files). Le ZIP contient uniquement ce patch indépendant, sans loader, jeu ni mods de tissus.

1. Quittez complètement le jeu.
2. Décompressez le ZIP. L'export de l'assistant contient la **langue de jeu enregistrée**, le dictionnaire, le cache et les corrections. Enregistrez un changement de langue avant d'exporter. Le paquet manuel de base sur GitHub est en chinois simplifié et ne contient que notre dictionnaire original.
3. Dans Steam, faites un clic droit sur le jeu puis Gérer → Parcourir les fichiers locaux. Utilisez la racine contenant déjà `BepInEx`, pas `Dressmaker.app/Contents`.
4. Copiez `BepInEx/plugins/DressmakerLanguages` du ZIP dans le dossier `BepInEx/plugins` du jeu.
5. Copiez `BepInEx/config/DressmakerLanguages` dans `BepInEx/config`. Créez `config` si nécessaire. **Copiez séparément ces deux sous-dossiers ; ne remplacez jamais BepInEx entier.**
6. Sauvegardez ailleurs les deux dossiers existants `DressmakerLanguages` avant de les remplacer. Gardez tous les autres plugins et mods.
7. Redémarrez le jeu.

Fichiers requis (`LANG` désigne la langue exportée, comme `zh-CN`, `ja` ou `fr`) :

```text
BepInEx/plugins/DressmakerLanguages/DressmakerLanguages.dll
BepInEx/config/DressmakerLanguages/runtime.json
BepInEx/config/DressmakerLanguages/known-sources.json
BepInEx/config/DressmakerLanguages/translations.LANG.json
```

Si Finder demande une autorisation, suivez macOS. Sinon, vérifiez Lire et écrire pour votre compte dans Lire les informations → Partage et permissions du dossier du jeu. N'accordez pas cet accès à tout le monde. Un appareil géré peut nécessiter un compte autorisé.

La copie manuelle ne donne pas de droit d'écriture à l'assistant. Vous pouvez toujours scanner, traduire et enregistrer le cache local. Tant que les droits restent limités, exportez à nouveau après de nouvelles traductions ou un changement de langue, quittez le jeu et copiez la mise à jour. Si le jeu ne peut pas écrire la configuration, la collecte de nouveaux textes en jeu peut échouer ; le scan des champs JSON courants reste disponible. Un redémarrage de l'assistant vérifie la présence du plugin et de sa configuration.

Pour désinstaller, quittez le jeu et retirez seulement les deux dossiers `DressmakerLanguages`. Gardez le dossier `data` de l'assistant pour conserver les traductions.

Un export local peut contenir vos noms de mods, corrections et traductions déjà présentes dans votre jeu. Pour une diffusion publique, utilisez le paquet de base généré par le script du projet.

La version 0.1.1 est préliminaire ; affichage et polices en jeu restent à vérifier. [Guides et remerciements](https://github.com/venti-klee/dressmaker-languages).
