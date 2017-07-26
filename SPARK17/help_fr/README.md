## Détails de la configuration des fichiers d'aide basés sur Jekyll pour ExpEYES-17

+ Les fichiers HTML générés sont enregistrés sous MD_HTML
+ Les fichiers d'aide d'usage général sont situés sous _utilities/
+ Les fichiers spécifiques aux applications sont situés sous _apps/


### tester la compilation localement

On peut utiliser Jekyll pour faire un serveur web local avec la commande `jekyll serve`.

Naviguer à `http://localhost:4000` pour accéder aux pages HTML générées. 

Les fichiers HTML statiques sont situés sous MD_HTML/, et sont chargés automatiquement par `spark17.py`


### À quoi doit ressembler le résultat final

![help_window](https://cloud.githubusercontent.com/assets/19327143/26511180/7396c32e-427e-11e7-88bb-92617c1c5f58.png)

Le générateur de site statique Jekyll est utilisé avec le CSS bootstrap.

les fichiers d'aide pour les expériences sont situés sous _apps/ en format Markdown
p.ex. `diode-iv.md`

```markdown
---
layout: e17page
title: Diode IV
date: 2017-05-21
description: Current-Voltage characteristics of PN junctions
imagebase: diode-iv
---
```
va automatiquement créer la page suivante. Cependant les images suivantes doivent aussi être présentes : photographs/diode-iv.jpg , screenshots/diode-iv.png, schematics/diode-iv.svg
![diode-iv](https://cloud.githubusercontent.com/assets/19327143/26511293/07696d90-427f-11e7-9729-f29d6ab2ca4d.png)


