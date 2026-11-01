# Compte rendu — Classification d’images par réseau de neurones
ce compte rendu reprend les résultats réels de mon exécution et répond aux six questions du TP:

## 1. Objectif

Développer un réseau de neurones capable de reconnaître trois formes géométriques : le cercle, le rectangle et le triangle, à partir d’images générées avec Python.

Le modèle est développé avec TensorFlow et Keras. Il est entraîné sur un ensemble d’images, puis évalué sur des données qui n'ont pas été utilisées pendant l'entraînement.

## 2. Données et prétraitement

Le jeu de données contient 3 000 images réparties en trois classes : 1 000 cercles, 1 000 rectangles et 1 000 triangles.

Les images sont chargées depuis les dossiers `knowledge/cercle`, `knowledge/rectangle` et `knowledge/triangle`.

L'exploration des images originales montre qu'elles sont au format PNG, avec des dimensions de 28 × 28 pixels et un mode colorimétrique RGBA. Elles sont ensuite converties en niveaux de gris avant d'être utilisées par le modèle.

Chaque image subit le même prétraitement :
- conversion en niveaux de gris ;
- redimensionnement en 28 × 28 pixels ;
- normalisation des valeurs des pixels entre 0 et 1 ;
- ajout d'une dimension correspondant au canal de l'image.

Chaque image est ainsi représentée par un tableau de dimensions 28 × 28 × 1.

Les données sont réparties en trois ensembles :
- entraînement : 2 100 images (70 %) ;
- validation : 450 images (15 %) ;
- test interne : 450 images (15 %).

Un second jeu de 60 images générées séparément permet également de vérifier les prédictions du modèle.

## 3. Architecture du modèle

Le modèle utilise un réseau de neurones convolutif (CNN), adapté à la reconnaissance d'images.

Son architecture comprend :
- une couche d'entrée de dimensions 28 × 28 × 1 ;
- deux couches convolutives utilisant l'activation ReLU ;
- deux couches de sous-échantillonnage MaxPooling ;
- une couche Flatten pour transformer les caractéristiques en vecteur ;
- une couche Dense de 64 neurones avec activation ReLU ;
- une couche de sortie de 3 neurones avec activation softmax.

La couche de sortie contient trois neurones, un par classe. La fonction softmax produit une probabilité pour chaque forme. La classe ayant la probabilité la plus élevée est retenue comme prédiction.

Le modèle comporte 105 411 paramètres entraînables.

## 4. Fonction de perte et optimiseur

L'entraînement utilise :
- **Fonction de perte :** `sparse_categorical_crossentropy`, adaptée à une classification multiclasse dont les étiquettes sont des entiers ;
- **Optimiseur :** `Adam`, qui ajuste les poids du réseau pendant l'apprentissage ;
- **Métrique :** `accuracy`, qui mesure la proportion de prédictions correctes.

L'entraînement est prévu sur 15 époques au maximum. Un mécanisme d'arrêt anticipé (`EarlyStopping`) surveille la perte de validation et restaure les meilleurs poids lorsque cela est nécessaire.

## 5. Résultats de l'évaluation

Après 15 époques, les résultats obtenus sur l'ensemble de test interne sont :

| Indicateur | Résultat |
|---|---:|
| Loss | 0,0353 |
| Accuracy | 99,11 % |

Sur les 450 images du test interne, environ 446 sont correctement classées.

Les résultats par classe sont également satisfaisants :
- cercle : rappel de 100 % ;
- rectangle : précision de 100 % et rappel de 99 % ;
- triangle : précision de 100 % et rappel de 99 %.

Le modèle a ensuite été évalué sur les 60 images du dossier `tests/`. Il a correctement classé les 60 images, soit une précision de 100 % sur ce jeu de test.

Ces résultats indiquent que le modèle reconnaît efficacement les formes présentes dans les données générées.

## 6. Surapprentissage et sous-apprentissage

La précision d'entraînement atteint 99,38 % à la dernière époque, tandis que celle de validation atteint 98,44 %. La perte de validation diminue au cours de l'entraînement.

L'écart entre les précisions d'entraînement et de validation reste faible. Les résultats ne montrent donc pas de signe évident de surapprentissage important.

Le modèle atteint également une précision élevée sur les données de test. Les résultats ne suggèrent pas de sous-apprentissage manifeste.

Ces observations concernent toutefois les données générées utilisées dans ce TP. Elles ne permettent pas de conclure que le modèle généralisera aussi bien sur des images très différentes.

## 7. Erreurs et améliorations possibles

L'analyse de la matrice de confusion montre que le modèle a correctement classé 446 images sur 450, soit une accuracy de 99,11 %.

Les erreurs observées sont les suivantes :
- **Cercles :** 150 images correctement classées sur 150, sans erreur.
- **Rectangles :** 148 images correctement classées sur 150. Deux rectangles ont été confondus avec des cercles.
- **Triangles :** 148 images correctement classées sur 150. Deux triangles ont été confondus avec des cercles.

Les quatre erreurs concernent donc des rectangles et des triangles prédits comme des cercles. Le modèle reconnaît parfaitement les cercles dans cet ensemble de test, mais présente quelques difficultés sur certaines images des deux autres classes.

Pour améliorer encore ses performances, plusieurs pistes pourraient être envisagées :
- augmenter la diversité des images d'entraînement ;
- varier davantage la taille, la position et l'orientation des formes ;
- utiliser des techniques d'augmentation des données ;
- tester le modèle sur des images réelles provenant d'une source différente.

Une limite importante reste que les images utilisées sont générées artificiellement. Les résultats obtenus ne garantissent donc pas la même précision sur des images réelles.

## 8. Conclusion

Le modèle obtient une précision de 99,11 % sur le test interne et de 100 % sur les 60 images de test générées séparément.

Les résultats sont satisfaisants pour ce jeu de données.Mais des tests sur des images plus variées seraient néanmoins nécessaires pour évaluer la capacité du modèle à généraliser à d'autres situations.