# STARTER-BACK

<img src="./doc/assets/genee.png" alt="Image 1" width="150px">

Starter-KIT est un projet de backend développé avec [Python](https://www.python.org/)
et [Flask](https://flask.palletsprojects.com/en/2.3.x/).

## informations globales

Genee est une entreprise Française, les documentations et les commits sont en français

## Dépendances Principales

- [Flask](https://flask.palletsprojects.com/en/2.3.x/) : Une micro framework pour Python.
- [SQLAlchemy](https://www.sqlalchemy.org/) : Un SQL toolkit et ORM pour Python.
- [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) : Une bibliothèque pour la conversion des types de
  données, la validation et la désérialisation.
- [Docker](https://www.docker.com/) : Une plateforme de conteneurisation.
- [Docker Compose](https://docs.docker.com/compose/) : Un outil pour définir et gérer des applications multi-conteneurs
  avec Docker.

## Structure du Projet

```markdown
.
├── app
│ │ └── Contient toute la logique de l'application
│ ├── data
│ │ └── Données (modèles SQLAlchemy) avec leur logique d'accès/modification (routes API, schémas)
│ ├── shared
│ │ └── Logique d'initialisation de l'application, modules partagés (fonctions utilitaires, services)
│ ├── config.py
│ │    └── Fichier contenant la configuration générale de l'application
│ ├── main.py
│ │    └── Point d'entrée de l'application Flask
│ ├── requirements.txt
│ │    └── Liste des librairies utilisées par l'application en fonctionnement normal
│ └── requirements-dev.txt
│      └── Liste des librairies utilisées lors du développement
├── doc
│ └── Décisions d'architecture (ARDs), guides, accumulation du savoir
├── envs
│   │└── Contient les fichiers nécessaires à l'exécution de l'application sur les différents environnements
│   ├── dev
│   │    └── Fichiers nécessaires à l'environnement de développement
│   ├── prod
│   │    └── Fichiers nécessaires à l'environnement de production
│   └── shared
│        └── Fichiers partagés entre les environnements
├── scripts
│   └── Utilitaires de lancement de l'application et liés aux tests
├── CONTRIBUTING.md
│   └── Contient les règles de codage du projet et des projets enfants
├── pyproject.toml
│   └── Contient la configuration des outils Black et iSort
└── README.md
```

Dans le répertoire `data`, chaque sous-répertoire représente une fonctionnalité (entité ou groupe d'entités reliées)
distincte de l'application.
Chaque module peut contenir les modules suivants :

- `controllers` : Définitions des points d'accès API pour le module. C'est ici que les requêtes HTTP sont reçues et
  dirigées
  vers les fonctions appropriés. Les routes sont regroupées dans un `flask.Blueprint`
- `models` : Modèles de données **SQLAlchemy** associés à la fonctionnalité.
- `schemas` : Schémas qui sont utilisés pour la validation des données entrantes pour le module.
- `services` : Classes utilitaire pour la logique métier associée à la fonctionnalité
- `test`: Contient les tests unitaires liés à la fonctionnalité

## Environnement de développement

### Prérequis

- Le sous-système Linux for Windows WSL2 est installé
    - dans Windows : Paramètres -> Applications -> Fonctionnalités facultatives -> Plus de fonctionnalités Windows ->
      cocher Sous-système Windows pour Linux puis redémarrer l'ordinateur
    - <https://learn.microsoft.com/fr-fr/windows/wsl/install>
- Git est installé sur la WSL2
    - Si vous êtes en télétravail, pensez à désactiver le VPN le temps de l'installation de Git
- Docker et Docker Compose sont installés sur la WSL2
    - https://medium.com/twodigits/install-docker-on-wsl-2-with-vpn-support-to-replace-docker-for-windows-45b8e200e171
- Python 3.10 est installé sur la WSL2
    - Recommandation : Utiliser pyenv et pyenv-virtualenv pour gérer vos installation de Python et vos environnements
      virtuels Python
        - <https://github.com/pyenv/pyenv>
            - Utiliser l’installeur automatique : <https://github.com/pyenv/pyenv-installer>
        - <https://github.com/pyenv/pyenv-virtualenv>
        - Ajouter les lignes suivantes au .bashrc
          ```shell
          export PYENV_ROOT="$HOME/.pyenv"
          command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
          eval "$(pyenv init -)"
          ```
        - Si vous avez choisi une distribution Debian, les librairies complémentaires suivantes nécessaires au
          fonctionnement du virtualenv doivent être installées:
          ```shell
          sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev liblzma-dev libpq-dev
          ```

- Le repository du test est clôné via le lien HTTPS

### Environnement virtuel Python

#### Création de l'environnement

Il est recommandé de créer un environnement virtuel Python dédié au projet afin qu'il soit utilisé en tant qu'
interpréteur sur votre IDE.
Pour cela, utiliser la librairie pyenv-virtualenv avec la commande suivante :

```shell
pyenv virtualenv <python_version> <virtualenv_name>
```

Exemple :

```shell
pyenv virtualenv 3.10.10 env-test
```

Basculer ensuite le terminal sur l'environnement virtual qui vient d'être créé :

```shell
pyenv activate <virtualenv_name>
```

Lier le répertoire courant à l'environnement virtual (fichier .python-version) :

```shell
pyenv local <virtualenv_name>
```

#### Installation des dépendances et des configurations

Installer les dépendances Python sur l'environnement virtual en exécutant la commande suivante :

```shell
pip install -r requirements.txt -r requirements-dev.txt
```

Installer les pre-commits Git avec la commande suivante :

```shell
pre-commit install
```

### Environnement Docker

L'installation de Docker se fait directement dans la WSL2 sans Docker Desktop for Windows depuis le passage en licence
payante de cette solution.

La procédure se base sur l'article
suivant : [Install Docker in WSL 2 without Docker Desktop](https://nickjanetakis.com/blog/install-docker-in-wsl-2-without-docker-desktop)

#### Suppression de l'installation actuelle

Si une ancienne installation de Docker a été faite, lancez les commandes suivantes pour la désinstaller.

```shell
# WSL
sudo apt remove docker-ce docker-ce-cli containerd.io
sudo rm -rf /mnt/wsl/shared-docker
sudo rm -rf /etc/docker
sudo rm -rf /var/lib/docker
```

Supprimer le bloc suivant du fichier `~/.bashrc`

```shell
DOCKER_DISTRO="Ubuntu"
DOCKER_DIR=/mnt/wsl/shared-docker
DOCKER_SOCK="$DOCKER_DIR/docker.sock"
export DOCKER_HOST="unix://$DOCKER_SOCK"
if [ ! -S "$DOCKER_SOCK" ]; then
    mkdir -pm o=,ug=rwx "$DOCKER_DIR"
    chgrp docker "$DOCKER_DIR"
    /mnt/c/Windows/System32/wsl.exe -d $DOCKER_DISTRO sh -c "nohup sudo -b dockerd < /dev/null > $DOCKER_DIR/dockerd.log 2>&1"
fi
```

#### Nouvelle installation de Docker

Exécuter les commandes suivantes pour installer Docker :

```shell
# WSL
# Install Docker, you can ignore the warning from Docker about using WSL
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add your user to the Docker group
sudo usermod -aG docker $USER

# Install Docker Compose v2
sudo apt-get update && sudo apt-get install docker-compose-plugin

# Sanity check that both tools were installed successfully
docker --version
docker compose version

# Using Ubuntu 22.04 or Debian 10 / 11? You need to do 1 extra step for iptables
# compatibility, you'll want to choose option (1) from the prompt to use iptables-legacy.
sudo update-alternatives --config iptables
```

Ajouter le contenu suivant dans votre fichier `~/.profile` :

```shell
if grep -q "microsoft" /proc/version > /dev/null 2>&1; then
    if service docker status 2>&1 | grep -q "is not running"; then
        wsl.exe --distribution "${WSL_DISTRO_NAME}" --user root --exec /usr/sbin/service docker start > /dev/null 2>&1
    fi
fi
```

Stopper votre WSL en lançant depuis Powershell la commande suivante :

```shell
# Powershell
wsl --shutdown
```

Puis relancer un terminal Debian/Ubuntu pour redémarrer la WSL2

#### Build des images

Lancer les commandes suivantes :

```shell
cd envs/dev
docker compose build
```

### Lancement de l'application

Ouvrez une invite de commande ou un terminal.

Accédez au répertoire "dev" situé dans le répertoire "envs" de l'application. Utilisez la commande suivante pour vous
déplacer vers ce répertoire :

```sh
cd /envs/dev
```

Une fois dans le répertoire "dev", exécutez la commande suivante pour démarrer l'application à l'aide de Docker
Compose :

```sh
docker-compose up --build
```

Une fois l'application démarrée, vous pouvez accéder à celle-ci en faisant vos requêtes
à `http://localhost:5001/api/<ROUTE>`.

## Variables d'Environnement

Le projet utilise les variable d'environnement suivantes:

- `DB_USER`: Nom de l'utilisateur BDD
- `DB_PASS`: Mot de passe de l'utilisateur BDD
- `DB_NAME`: Nom de la BDD
- `DB_IP`: Adresse de la BDD
- `MIGRATIONS` : Cette variable détermine si des migrations doivent être effectuées sur la base de données.
  Mettez-la à `1` pour activer les migrations et à `0` pour les désactiver.

Ces variables sont à définir dans un fichier .env, situé à còté du Dockerfile de son environnement (`envs/dev/back/.env`
et `envs/prod/back/.env`)\
Comme les .env contiennent souvent des données sensibles, ces fichiers ne sont pas versionnés.\
Pour démarrer le développement, créer un `.env` en copiant le `.env.example` situé au même endroit.

## Lancement de l'application en mode développement

Ouvrez une invite de commande ou un terminal.

```shell
docker-compose -f envs/dev/docker-compose.yml up 
``` 

Ne pas oublier de créer le fichier `.env` à ``envs/dev/back/.env``

## Gestion des dépendances

La gestion des dépendances du projet utilise pip-tools. Cet outil permet, à la manière des package-lock.json sur les
projets Node, de freeze la totalité des dépendances (directes et indirectes) du projet.

pour installer pip-tools :

```shell
pip install pip-tools
```

Les dépendances directes sont spécifiées dans le fichier `pyproject.toml`à la racine du projet.

Les fichiers requirements.txt et requirements-dev.txt situés dans le dossier app ne doivent pas être modifiés
manuellement.

En cas de changement de dépendance directe (ajout, modification, suppression) :

- Modifier le fichier pyproject.toml
    - Si la dépendance sert au fonctionnement nominal de l'application
        - Toucher à la section [project] > dependencies
        - Lancer les commandes suivantes :
          ```shell
          pip-compile --upgrade --output-file=app/requirements.txt pyproject.toml
          pip-compile --upgrade --extra=dev --output-file=app/requirements-dev.txt pyproject.toml
          ```
        - Si la dépendance sert uniquement à l'environnement de dev ou de CI
            - Toucher à la section [project.optional-dependencies] > dependencies
            - Lancer la commande suivante :
          ```shell
          pip-compile --upgrade --extra=dev --output-file=app/requirements-dev.txt pyproject.toml 
          ```

La commande pip-compile permet de générer les fichiers requirements.txt et requirements-dev.txt, qui contiennent les
dépendances
directes et indirectes et leurs versions figées.

## Configuration de Pycharm

Pycharm est l'IDE Python de jetbrains, pour avoir acces au programme par l'IDE sans erreurs demande quelque
modification

> **NOTE**: cette configuration a été faites avec la nouvelle UI de Pycharm elle peut ne pas fonctionner sur l'ancienne

### Selection de l'interpreteur python du service docker (permet d'avoir la complétion sans avoir à installer les dépendences sur l'hôte)

- Cliquer sur le bouton de l'interpréteur en bas a droite (là où il y a probablement écrit ``Python 3.X`` avec la
  version de python installée sur l'hôte)
- ``Add New Interpreter``, puis choisir ``On Docker Compose...``
- Dans le champ ``Configuration files`` sélectionner le fichier suivant: ``envs/dev/docker-compose.yml``
- Dans le champ ``Service``, choisir le nom du service qui contient flask, i.e. ``flask`` (le champ devrait avoir des
  valeurs disponibles apres avoir fini l'étape précédente)
- Appuyer sur ``Next``, attendre la fin de commande lancée par l'IDE puis ``Next``
- Appuyer sur ``Create`` dans la dernière fenêtre
- Si en bas a gauche il y a ecrit ``Remote Python 3.X Docker Compose (flask)``, vous avez tout pour commencer !

### Mise en place de la visualisation de la base de donnée

Cliquez sur le logo qui ressemble a une pile de disque sur le coté droit.\
Si vous ne le voyez pas, assurez vous que le plugin ``Database tools and SQL`` soit bien installé.\
Une fois le menu ouvert, cliquez sur ``+ > Data Source > PostgreSQL``\
Mettez les informations suivantes :

- ``port: 5432``
- ``host: localhost``
- ``connect with user and password``
    - user: ``postgres``
    - password: ``postgres``

> **NOTE**: assurez vous bien pendant la connexion avec le docker postgres que le docker soit lancé

Une fois connecté vous verrez a droite ``postgres@localhost`` et plus a droite un petit bouton avec écrit quelque choise
du genre ``1 of 4`` ou bien ``4``, cliquez dessus.\
Cochez ``db_dev`` et ``All schemas`` dans le menu déroulant de ``db_dev``\
Vous pouvez maintenant accéder à toutes vos table dans ``postgres@localhost > db_dev > public > tables``

## Explication des scripts

Les scripts sont situés dans le dossier ``scripts/``

- ``application_restart.sh``
    - Relance l'application tout en effaçant les données de la base de données
    - Fait en sorte que l'application se relance automatiquement apres un Ctrl-C
- ``*.http``
    - Permet de prototyper des requetes pour tester l'application et peupler la base de données facilement exactement
      comme Postman
    - Pycharm permet de lancer chaque requete du fichier indépendamment (bouton 'Play' a gauche de la requete) ou toutes
      les requetes (bouton 'Double Play' en haut du fichier)
    - Important : les requêtes doivent être séparées par une ligne avec 3 hashtags ('###')

## Mise en place du format par lint

``black`` permet de formatter le code. Pour le relier à la fonction ``format code`` de l'IDE:

- S'assurer que Black est bien installé : ``python3 -m pip install Black``
- Aller dans ``Settings... > Tools > Black`` et activer ``on code reformat``
