# Dressmaker · Assistant multilingue pour mods

[简体中文](README.zh-CN.md) · [English](README.md) · [日本語](README.ja.md) · [한국어](README.ko.md) · [Français](README.fr.md) · [Deutsch](README.de.md) · [Español](README.es.md)

Un outil macOS indépendant qui traduit l’interface Yuuma ModLoader et les textes anglais des mods. **La version 0.1.1 est préliminaire : l’intégration dans le jeu n’a pas encore été testée.**

## Fonctions

- Langues distinctes pour le jeu et l’interface : chinois, anglais, japonais, coréen, français, allemand et espagnol.
- Dictionnaires, corrections et cache hors ligne ; modèles Argos facultatifs pour les phrases inconnues.
- MyMemory sans clé, adaptateur web Bing expérimental ou instance LibreTranslate disponible.
- Analyse des champs JSON courants des nouveaux mods et collecte de l’anglais affiché dans le jeu.
- Cache par langue, priorité aux corrections manuelles et protection des variables et balises.

## Pour les joueurs

1. Installez [Yuuma ModLoader pour Mac](https://www.nexusmods.com/dressmaker/mods/1?tab=files).
2. Téléchargez **Dressmaker-Languages-Mac-0.1.1.zip** dans les Releases du dépôt et extrayez tout le dossier. Python 3.9 ou plus récent est requis.
3. Ouvrez `Start.command` ou `针影裁梦多语言助手.app`.
4. Choisissez la langue de l’assistant, vérifiez le dossier et la langue du jeu, enregistrez, installez le correctif puis redémarrez le jeu.
5. Analysez après chaque nouveau mod et gardez l’assistant ouvert pour traduire. Les résultats sont modifiables.

Consultez le [guide français](docs/fr.md) pour les modèles, la désinstallation et les données. Download ZIP sur GitHub fournit les sources sans plugin compilé ni `.app`. Les joueurs doivent utiliser l’archive Release.

## Portée et vérification

L’analyse reconnaît `name`, `displayName`, `display_name`, `description`, `tooltip` et `title` dans les fichiers JSON. Les hooks ciblent Unity Text / TextMeshPro dans le gestionnaire ou les noms découverts. Les interfaces personnalisées, images, formats binaires spéciaux et sources non anglaises ne sont pas garantis. L’outil n’ajoute pas de tissus et ne localise pas entièrement le jeu de base.

Le plugin a été compilé pour ModLoader 0.7.3 / BepInEx 5.4.23.5 / Unity 6000.3.4f1. Les 28 tests automatisés ont réussi. Le changement de langue local a été vérifié et Bing et MyMemory ont fourni des traductions réelles. Les adaptateurs web peuvent échouer selon le réseau, les limites et les changements de page. Les noms de tissus tiers, la disposition et les polices en jeu restent à vérifier.

Le mode en ligne envoie les textes anglais inconnus au service choisi. Les requêtes sont espacées d’au moins 3 secondes ; le budget par défaut est de 4 500 octets UTF-8 par jour. Un échec conserve l’original. Le repli MyMemory est désactivé par défaut ; les deux essais comptent dans le budget lorsqu’il est activé. Le dictionnaire et le cache restent utilisables hors ligne.

## Développement et contributions

Les sources sont dans `src/` et `assistant/`. L’assistant de base utilise uniquement la bibliothèque standard Python.

```sh
python3 -m unittest discover -s tests -v
```

La compilation nécessite vos propres assemblages du jeu et du loader ainsi qu’un SDK .NET. L’assistant est en 0.1.1 et le plugin inchangé garde sa version interne 0.1.0. Les vérifications GitHub Actions sont activées ; consultez la page Actions du dépôt pour leurs résultats.

Les Issues et Pull Requests sur les termes, polices et compatibilités sont bienvenues. Indiquez les versions du jeu, du système et du loader et un exemple publiable. Modifiez les sept catalogues et guides si vous changez un texte. Ne publiez pas de sauvegardes, mods privés ou ressources du jeu.

## Publier sur GitHub

1. Créez un dépôt **Public** vide. Ne générez pas un second README ni une licence : ils sont fournis.
2. Extrayez **Dressmaker-Languages-GitHub-0.1.1.zip** et importez son contenu avec `README.md` à la racine. Incluez `.github/`, `.gitignore` et `.gitattributes`. Finder affiche les fichiers cachés avec `Command + Shift + .`. Git préserve les permissions d’exécution des scripts.
3. Créez une Release `v0.1.1` et joignez l’archive Mac. Les sources vont dans le dépôt ; l’archive Mac sert aux joueurs.
4. Vérifiez le correctif dans votre jeu avant publication et actualisez les résultats. Données personnelles, chemins, jetons et historique Git sont exclus. 

La liste exacte est dans `UPLOAD-MANIFEST.json`. Les instructions officielles de GitHub figurent ci-dessous.

Instructions officielles GitHub: [Create repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository) · [Upload files](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository) · [Create Release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)

## Crédits et licence

Implémentation indépendante inspirée des [fonctions publiques de l’outil SallyHCA](https://www.nexusmods.com/dressmaker/mods/339), sans son code, ses dictionnaires ni ses ressources. Le code original et les dictionnaires rédigés sont sous [MIT](LICENSE), sans droits sur les ressources du jeu ou du projet cité. Aucune affiliation avec le jeu, Nexus Mods, Microsoft ou Argos.

## Remerciements

Merci aux auteurs et aux équipes qui ont rendu ce projet possible :

- [Cozy Lives (développement) et Free Lives (édition)](https://store.steampowered.com/app/4019220/Dressmaker/) — Merci d’avoir créé et publié Dressmaker, où chacun peut concevoir, couper et coudre ses vêtements.
- [Yuumeow — Yuuma’s Dressmaker ModLoader](https://www.nexusmods.com/dressmaker/mods/1) — Merci pour le loader et la prise en charge des contenus personnalisés qui permettent aux créateurs de partager tissus et accessoires.
- [SallyHCA — Outil de localisation chinoise automatique](https://www.nexusmods.com/dressmaker/mods/339) — Merci d’avoir partagé une méthode pour traduire le gestionnaire et les noms des contenus. Votre outil et sa présentation publique ont inspiré le parcours de traduction de ce projet.

Cette implémentation est indépendante ; ces remerciements ne supposent aucune approbation des auteurs. Leurs programmes, dictionnaires, ressources du jeu et modèles ne sont pas redistribués ici.


## Télécharger le paquet pour installation manuelle

Exportez le plugin, le dictionnaire et les traductions de la langue de jeu enregistrée, sans écrire dans le dossier du jeu. Exportez à nouveau après une traduction ou un changement de langue. Le ZIP contient les instructions en sept langues. [Télécharger le paquet pour installation manuelle](docs/manual-fr.md).
