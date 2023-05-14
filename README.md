# *Simulation d'une machine neuronale mind 1024 (32x32)*
## Introduction : simulation et application
Le but de ce projet étant la simulation d'une machine neuronal MIND 1024, nous avons choisi comme application pour notre simulation une classification des chiffres manuscrit. Nous pourrons ensuite conclure quant aux performances du MIND 1024, ses limites .., mes surtout quant à ce qu'on peut faire avec 1024 neuronnes.
## Simulation du MIND 1024
Pour simuler le MIND 1024, j'ai commencé par la documentation. Malgré  le peu de ressources j'ai décidé de prendre comme point de départ le réseau de Hopfield. 
Un réseau de Hopfield est un réseau de neuronnes sans couches, et où tous les neuronnes sont connectés. Il s'agit d'une mémoire associative qui est utilisée pour retrouver une version non bruitées d'une entrée donnée sur la base de pattern mémorisé par le réseau (entraînement). La capacité d'un réseau de Hopfield est le nombre de pattern qu'on peut mémoriser et elle est fortement liée à son nombre de neuronnes (109 patterns pour 1024 neuronnes). 
## Data
Pour le moment, on utilise 784 neuronnes, 28*28 pixels pour les images. la capacité théorique du réseau est de 80.
On utilisera alors MNIST dataset comme training set et peut-être même pour évaluer les performances du modèle.
En cliquant sur le bouton "show-training-set" on obtient ceci : 
![Alt text](bin/training_dataset.png)
*Remarque : si plus tard on souhaite utiliser moins de neuronnes, donc moins de pixels pour nos images. On pourra se tourner vers [sklearn.datasets.load_digits](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html) (size 8x8) ou même utiliser [convolutional layers](https://machinelearningmastery.com/convolutional-layers-for-deep-learning-neural-networks/) ou auto-encoders*
## Début du projet 
#### 1er problème : 
Le réseau ne converge vers aucun des patterns
#### 2eme problème :
pour NUMBER_DIGITS = 10, on obtient des résultats de classifications très mauvais.
![Alt text](bin/MIND1024_1.png)
#### 3eme problème :
Ce dernier peut être résolu si on a convergence vers les patterns (ce qui devrait être le cas dans un réseau de Hopfield, sauf spurious states), le problème est d'afficher comme output le label, et pas le pattern après classification.
## Ressources
[hopfield_mnist](https://github.com/kencyke/hopfield-mnist) est une belle tentative. A utiliser pour comparer à mes résultats
#### Pour 3 patterns : 
![Alt text](bin/animation.gif)
#### Pour 10 patterns :
![Alt text](bin/animation10.gif)
On montre la différence entre l'itération 26 et la dernière :
![Alt text](bin/26.png)
![Alt text](bin/79.png)
D'où l'importance d'ajouter une condition d'arrêt indépendante du nombre d'itérations qu'on s'est fixé 
### on relance le même script pour 3 pattern en affichant leur label et les patterns d'entraînement 
![Alt text](bin/Training_data.png)
![Alt text](bin/animation_.gif)
## Stable states and spurious states : 
Ces notions sont très importantes. En effet si le modèle est bien, les patterns d'entraînement seront des états stables, cad que on iterant sur un tel état on change rien. 
#### On peut penser à ajouter quelques lignes de code à la fonction de synchronisation du réseau :
for i in range(self.patterns):
  if x == train[i] :
    print('stable state %i' % target[i])
#### faudra aussi implémenter le code .py dans notre site web
## Remarque générale 
Dans les réseaux de neuronnes on a vu que initialiser les poids avec 0 peut causer des problèmes (signals faibles) et avec des grandes valeurs (overflow). Aussi faut voir le choix de la fonction d'activation et les algos qui mettent à jour les poids.


## algo :
pour eliminer les spurious states, on utilise Storkey comme learning method pour notre reseau de Hopfield.
Cependant cela marche tres bien pour 2 pattern, moins bien pour 3. Et pour plus on remarque que le reseaux converge toujours vers le dernier pattern entrainé.
On essayera de revoir l'algo de convergence et peut etre utiliser backward propagation ou gradient descent.
## Version finale
Après avoir vu que Hebbian learning ne donne pas les résultats attendus pour la classification MNIST. J'ai trouvé un meilleur algorithme mais trés couteux en calcul.
Les résultats sont maintenant satisfaisant :
- accuracy unnoise : entre 0.99 et 1
- accuracy classify : entre 0.6 et 0.75


![Alt text](screen app.png)

