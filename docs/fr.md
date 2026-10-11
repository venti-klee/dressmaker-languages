# Assistant multilingue Dressmaker 0.1.5

[简体中文](zh-CN.md) · [English](en.md) · [日本語](ja.md) · [한국어](ko.md) · **Français** · [Deutsch](de.md) · [Español](es.md)

Un assistant Mac indépendant et un correctif pour traduire l’interface de Yuuma ModLoader et les noms affichés des objets ajoutés par les mods. Il s’inspire des fonctionnalités publiques de [l’outil de SallyHCA](https://www.nexusmods.com/dressmaker/mods/339) et de [son projet](https://github.com/Sally-4869/dressmaker-mods-cn). Aucun code, dictionnaire ou autre ressource de ce projet n’est inclus.

Download ZIP de GitHub contient les sources sans plugin compilé ni `.app`. Les joueurs doivent utiliser la Release Mac ; les utilisateurs des sources doivent compiler selon les instructions ci-dessous. Publication : [README](../README.fr.md).

## Installation

1. Installez d’abord la [version Mac de Yuuma ModLoader](https://www.nexusmods.com/dressmaker/mods/1?tab=files). Le correctif a été compilé avec la version 0.7.3 installée sur cet ordinateur.
2. Extrayez le paquet complet dans un dossier accessible en écriture. Python 3.9 ou ultérieur est nécessaire. Les fonctions de base n’exigent aucune bibliothèque Python supplémentaire ni environnement .NET.
3. Ouvrez `Start.command` ou `针影裁梦多语言助手.app`. Une page locale s’ouvre dans le navigateur. Gardez la fenêtre de commande ouverte pendant l’utilisation.
4. Sélectionnez **Langue de l’assistant** en haut de la page. Les textes de l’interface et le lien du guide changent immédiatement, et votre choix est mémorisé dans ce navigateur. Cela ne modifie pas la langue de traduction du jeu. Au premier lancement, la langue du navigateur est utilisée, avec l’anglais comme langue de repli.
5. Vérifiez le dossier du jeu, choisissez **Langue de traduction du jeu**, puis cliquez sur **Enregistrer les paramètres**. La langue cible initiale du jeu est le chinois simplifié.
6. Cliquez sur **Installer / mettre à jour le correctif**. Seuls les dossiers dédiés `BepInEx/plugins/DressmakerLanguages/` et `BepInEx/config/DressmakerLanguages/` sont créés ou mis à jour.
7. Sauvegardez votre progression puis redémarrez le jeu normalement. Vérifiez le résultat dans Mod Manager ou Mod Settings. Les changements suivants de dictionnaire et de langue s’appliquent généralement aux textes collectés en environ 2 secondes.
8. Après l’installation de nouveaux mods, cliquez sur **Analyser les mods et le gestionnaire**. Le correctif collecte aussi les textes anglais inconnus affichés dans le jeu.

Pour une installation manuelle, copiez le dossier fourni `BepInEx/plugins/DressmakerLanguages/` à l’emplacement correspondant du jeu, puis utilisez le bouton d’installation de l’assistant pour générer la configuration. Les assistants Windows `.exe` et Vortex ne sont pas nécessaires.

## Langues et couverture

L’interface de l’assistant et les guides Markdown sont disponibles en chinois, anglais, japonais, coréen, français, allemand et espagnol. La langue de l’interface et celle des traductions du jeu sont indépendantes.

Les dictionnaires du jeu comprennent 148 termes courants pour chacune des langues chinoise, japonaise, coréenne et française, et 14 pour l’allemand et l’espagnol. Le chinois et le japonais importent aussi les tables officielles de votre propre installation du jeu. Cet ordinateur a généré 5 157 entrées chinoises ; ce nombre dépend de la version du jeu. Les traductions officielles sont générées localement et ne sont pas distribuées dans l’archive. L’anglais rétablit le texte d’origine.

Chaque langue cible possède son propre cache. Le correctif traduit les textes affichés des mods ; il ne fournit pas une localisation complète du jeu de base dans de nouvelles langues.

## Traduction hors ligne et en ligne

Les corrections manuelles sont prioritaires. Les autres entrées suivent cet ordre : **dictionnaire → traduction en cache → combinaison de termes entièrement reconnus → modèle Argos hors ligne installé → service gratuit en ligne**.

Les dictionnaires et traductions enregistrées fonctionnent immédiatement hors ligne. Une combinaison de termes n’est traduite que si chaque mot est reconnu. Sans modèle ni service en ligne, un texte inconnu reste en anglais dans la liste des textes à traduire.

Pour traduire des phrases inconnues hors ligne, choisissez la langue cible du jeu puis cliquez sur **Télécharger le modèle hors ligne de cette langue**. La première installation télécharge un environnement Python isolé et un modèle : elle nécessite Internet et peut prendre du temps. Une fois terminée, quittez puis relancez l’assistant. Désactivez la traduction en ligne et enregistrez les paramètres pour travailler entièrement hors ligne. Chaque langue nécessite son propre modèle, selon les disponibilités de l’index Argos. Les modèles ne sont pas inclus dans l’archive et leur procédure d’installation n’a pas encore été testée de bout en bout.

Le service par défaut est l’API publique de MyMemory, sans clé API. Ses quotas s’appliquent. L’assistant ajoute un budget prudent de 4 500 octets UTF-8 par jour, un espacement des requêtes et une pause après un échec. Une requête gratuite accepte au maximum 500 octets ; utilisez un modèle hors ligne ou une traduction manuelle pour les textes plus longs. Vous pouvez fournir une instance LibreTranslate HTTPS disponible, sans garantie de gratuité ni de disponibilité permanente.

En mode en ligne, seuls les textes anglais affichés sans traduction locale sont envoyés au fournisseur choisi, jamais les sauvegardes ou les paquets de mods. Les résultats réussis sont enregistrés. Un problème de connexion, un quota ou une réponse invalide laisse le texte d’origine intact. Aucun mécanisme d’usurpation ou de contournement des paiements ou CAPTCHA n’est prévu.

## Services de traduction gratuits

Choisissez un service puis cliquez sur **Enregistrer les paramètres**.

- **MyMemory** : API publique par défaut, sans clé. Les quotas du fournisseur s’appliquent.
- **Adaptateur web Bing (expérimental)** : sans clé. Il obtient une session temporaire depuis la page publique de traduction et l’utilise pour traduire. Ce n’est pas une API officielle stable ; des changements de page, de session ou de limites peuvent l’interrompre.
- **LibreTranslate** : indiquez une instance HTTPS que vous pouvez utiliser. Son coût et ses exigences de compte dépendent de l’instance. Seules les instances sans clé sont actuellement prises en charge.

L’option de repli vers MyMemory est désactivée par défaut. Elle effectue un seul essai après une erreur réseau ou une indisponibilité du service, jamais pour un budget dépassé, un texte trop long, un format endommagé ou une adresse vide. Le même texte peut être envoyé à deux services ; chaque essai compte dans le budget quotidien. Les requêtes sont espacées d’au moins 3 secondes. Des échecs répétés déclenchent une pause de 5 minutes, sans remplacer le texte original. Les dictionnaires et le cache restent disponibles hors ligne.

La session Bing reste en mémoire. Aucune connexion à un compte, conservation de compte, rotation de proxy ou résolution de CAPTCHA n’est utilisée. Les résultats valides sont conservés par langue cible ; les corrections manuelles restent prioritaires.

Les 66 tests automatisés ont réussi : session, code du chinois, réponses invalides, cache hors ligne, repli et budget. Bing a fourni des traductions réelles en chinois, japonais, coréen, français, allemand et espagnol. Le cache hors ligne et la conservation de `{0}` ont été vérifiés. Des erreurs de connexion et délais dépassés ont aussi eu lieu ; l’adaptateur reste expérimental.

## Correction et désinstallation

Recherchez le texte anglais, modifiez la traduction puis cliquez sur **Enregistrer**. Une correction manuelle remplace les traductions automatiques et le dictionnaire pour cette langue. Conservez les variables, sauts de ligne et balises de mise en forme ; les traductions qui les altèrent sont refusées. Changer la langue de l’assistant conserve les brouillons de traduction non enregistrés.

 **Traduire les textes manquants** traite aussi les chaînes candidates du gestionnaire. Le mode automatique privilégie les textes réellement affichés et le contenu des mods, plutôt que les chaînes inutilisées du programme.

Cliquez sur **Désinstaller le correctif**, puis redémarrez le jeu. Les dossiers du plugin et de la configuration sont déplacés dans `data/backups/`. Les traductions sont conservées. Le correctif ne modifie pas le chargeur d’origine, les mods, les identifiants, les textures ou les sauvegardes.

## Fichiers locaux

- `data/translations.sqlite3` : cache et corrections par langue.
- `data/settings.json` : langue cible, options en ligne et chemin du jeu.
- `data/model-install.log` : journal d’installation des modèles.
- `.venv/` et `models/` : environnement et modèles facultatifs.
- Dans le jeu, `BepInEx/config/DressmakerLanguages/pending.jsonl` : textes inconnus collectés.
- Dans le jeu, `BepInEx/LogOutput.log` : recherchez `Dressmaker Languages` pour les problèmes de chargement ou de polices.

La page est accessible uniquement sur l’ordinateur local. Un jeton de session aléatoire protège les opérations d’écriture. Après la fermeture de l’assistant, les dictionnaires et traductions publiés restent utilisables par le correctif. La traduction automatique nécessite que l’assistant reste ouvert.

## Vérification et limites

Le plugin a été compilé avec ModLoader 0.7.3, BepInEx 5.4.23.5 et Unity 6000.3.4f1. Onze tests du moteur de traduction ont réussi. Des requêtes réelles à MyMemory ont renvoyé des traductions chinoises, japonaises, coréennes et françaises. La localisation de l’interface et des guides a été ajoutée en version 0.1.5.

**L’intégration dans le jeu n’a pas encore été testée.** La couverture des textes, la disposition, les polices japonaises et coréennes et les noms de tissus tiers restent à vérifier. Aucun paquet de contenu n’était installé sur cet ordinateur pendant le développement.

Le correctif utilise les voies habituelles d’affichage Unity Text / TextMeshPro. Le texte dessiné spécialement, intégré aux images, les sources autres que l’anglais et la réécriture directe des scripts narratifs ne sont pas garantis. Les fichiers narratifs ne sont pas modifiés. Les termes textiles, les qualificatifs de couleur ou la grammaire peuvent être mal traduits ; corrigez-les au besoin.

## Sources et compilation

Le plugin se trouve dans `src/DressmakerLanguages.cs`, et l’assistant dans `assistant/`. Utilisez votre propre SDK .NET et les fichiers d’assemblage du jeu :

```sh
python3 src/build.py --game "/path/to/game" --dotnet "/path/to/dotnet"
```

Le code indépendant et les dictionnaires rédigés pour cet outil sont sous licence MIT. Cette licence ne confère aucun droit sur les ressources du jeu ou du projet de référence.

## Remerciements

Merci aux auteurs et aux équipes qui ont rendu ce projet possible :

- [Cozy Lives (développement) et Free Lives (édition)](https://store.steampowered.com/app/4019220/Dressmaker/) — Merci d’avoir créé et publié Dressmaker, où chacun peut concevoir, couper et coudre ses vêtements.
- [Yuumeow — Yuuma’s Dressmaker ModLoader](https://www.nexusmods.com/dressmaker/mods/1) — Merci pour le loader et la prise en charge des contenus personnalisés qui permettent aux créateurs de partager tissus et accessoires.
- [SallyHCA — Outil de localisation chinoise automatique](https://www.nexusmods.com/dressmaker/mods/339) — Merci d’avoir partagé une méthode pour traduire le gestionnaire et les noms des contenus. Votre outil et sa présentation publique ont inspiré le parcours de traduction de ce projet.

Cette implémentation est indépendante ; ces remerciements ne supposent aucune approbation des auteurs. Leurs programmes, dictionnaires, ressources du jeu et modèles ne sont pas redistribués ici.


## Télécharger le paquet pour installation manuelle

Exportez le plugin, le dictionnaire et les traductions de la langue de jeu enregistrée, sans écrire dans le dossier du jeu. Exportez à nouveau après une traduction ou un changement de langue. Le ZIP contient les instructions en sept langues. [Télécharger le paquet pour installation manuelle](manual-fr.md).


## Progression des traductions

Mise à jour chaque seconde. La progression compte les textes traités ; originaux conservés et échecs ne sont pas des traductions réussies. La liste se met à jour et conserve les modifications non enregistrées.

## Google web et traductions enregistrées

Les requêtes web Google ne nécessitent aucune clé. La disponibilité dépend du réseau ; des modifications de page ou des limites peuvent entraîner des échecs. Les requêtes sont espacées d’au moins 3 secondes.

Exemple : Aujourd’hui (UTC) : 4,498 / 4,500 octets utilisés · 2 restants. Il s’agit du budget local ; l’augmenter ne relève pas le quota du service.

Les traductions sont enregistrées localement et réutilisables hors ligne. Conservez le dossier data lors des mises à jour ; les caches par langue et les corrections restent enregistrés.

## Recherche et filtres du dictionnaire (0.1.4)

La recherche porte sur l’original et la traduction enregistrée. Les résultats se mettent à jour pendant la saisie ou avec Entrée. La liste réunit les textes collectés, le dictionnaire et le cache de la langue cible actuelle, avec une ligne par original.

- **État** : non traduit, traduit ou original conservé. Le décompte utilise les valeurs enregistrées effectivement appliquées ; les modifications non enregistrées ne comptent pas comme des traductions réussies.
- **Canal** : dictionnaire, termes combinés, correction manuelle, modèle hors ligne, Google, Bing, MyMemory ou LibreTranslate. Le canal affiché est celui utilisé, notamment dictionnaire lorsqu’il remplace une ancienne traduction automatique.
- **Origine** : tous les textes, textes collectés, affichés en jeu, contenus des mods, chaînes candidates du gestionnaire, ou dictionnaire/cache uniquement. Combinez « Non traduit » et « Textes affichés en jeu » pour repérer les traductions manquantes visibles.
- **Tri et pages** : original croissant/décroissant, enregistrements récents ou textes du jeu en premier ; 25, 50 ou 100 lignes par page et accès par numéro. Un message explique les résultats vides ; effacez les filtres pour réinitialiser.

Les filtres et les pages conservent les modifications non enregistrées et affichent leur nombre. Enregistrez chaque ligne avant de fermer ou de recharger la page : les brouillons non enregistrés sont perdus au rechargement. Une ligne enregistrée peut quitter le filtre actuel. La recherche et les filtres ne contactent aucun service de traduction et ne consomment pas de budget.

Les filtres ne concernent que la liste ; la traduction des textes manquants traite la file collectée.

Le décompte distingue textes affichés en jeu, contenus de mods, candidats du gestionnaire et entrées du dictionnaire/cache seules. L’analyse peut collecter formats internes, erreurs et textes inutilisés : les candidats ne représentent pas des omissions visibles. Le mode automatique traite les textes affichés et les mods. Filtrez Non traduit + Textes affichés en jeu pour vérifier les textes collectés ; ouvrez les écrans non visités pour les collecter.

Un échec du service suspend le lot et laisse le reste non traité. Après la pause, les tâches inachevées sont retentées avec la même langue et le même périmètre, y compris les candidats lancés manuellement. Cliquer à nouveau ne contourne pas la pause et ne réinitialise pas la progression. Changer les réglages annule l’ancienne tentative. Seules les traductions enregistrées avec succès réduisent le décompte.

Correction des espaces de début et de fin avec Google : le corps est envoyé et vérifié intégralement, puis les espaces sont restaurés. Une réponse correcte n’est plus rejetée pour des espaces supprimés ; balises, variables et intégrité du corps restent protégées.
