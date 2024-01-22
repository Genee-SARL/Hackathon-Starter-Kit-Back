# MQL-BACK

<img src="./doc/assets/genee.png" alt="Image 1" width="150px">

MQL-BACK est un projet de backend développé avec [Python](https://www.python.org/)
et [Flask](https://flask.palletsprojects.com/en/2.3.x/).

## Gestion de version Git

- Respect du [Git Flow](https://www.atlassian.com/fr/git/tutorials/comparing-workflows/gitflow-workflow) :
    - Une branche "develop" commune aux développements en cours
        - Chaque branche de dev part de la branche "develop"
    - Une branche "release" de recette
    - Une branche "master" de production

- Gestion des commits
    - Commits "utiles" uniquement (pas de succession de commits "Fix TU")
    - Messages de commit en français

## Style

- Suivi des règles du PEP8
    - La longueur des lignes a été augmenté à 140 caractères pour encourager les noms de méthode explicites
- Le code est inspecté/clean à chaque commit grâce au pre-commit exécutant 3 outils
    - [Black](https://black.readthedocs.io/en/stable/) qui re-formatte le code suivant les règles de PEP8
    - [Flake8](https://flake8.pycqa.org/en/latest/) qui suit également les règles de PEP8 et annule le commit en cas
      d'erreur de lint
    - [iSort](https://pycqa.github.io/isort/) qui reformatte les imports

> **INFO** : Lors d'un commit, si Black reformate un fichier, alors le pre-commit sera failed. C'est normal, car Black
> estime que
> si un fichier est modifié, alors il ne doit pas être commit automatiquement.
> Dans ce cas, relancer le commit et celui-ci passera.

- Le code est ensuite une nouvelle fois analysé par SonarQube
    - Si l'analyse Sonar fail, la branche ne peut être mergée

### Règles plus précises

- Ce qui est en lien avec le métier en français, le reste en anglais
- Attention à l'abus de commentaires : Python est très expressif et un bon code avec de
  méthodes explicites se comprend de lui même la plupart du temps
- Attention a ne pas dupliquer du code, pensez à réutiliser ou factoriser
    - Make it Work, Make it Right, Make it Fast
- Prendre le temps de tout nommer correctement
- Pas de `except` global ou de `except Exception`
- Pas de fonction trop longue (~30 Lignes)
- Pas de fichier trop long (~300 Lignes)
- Pour les chaînes de caractères comportant des variables : utiliser les fstring plutôt que % ou format :

```python
exemple = f'le texte avec {une_variable} en utilisant les f-string'
```

- Sur les API de listes, préférer un retour de liste vide en 200 plutôt qu'une erreur si jamais
  aucun résultat n'est trouvé.
- Les chaînes en dur doivent être extraites dans des constantes si elles sont réutilisées
- Les noms de variables doivent être pertinents et explicites
- Attention au code mort !

## Process de dev

- Pour les chantiers moyens à gros, réalisation d'un DCT avant de débuter les développements
- Lorsqu'un choix technique doit être réalisé (ex.: choix d'une librairie plutôt qu'une autre), écriture d'un
  ADR (Architecture Decision Record)
- Profiter des chantiers pour mettre à jour les versions mineures des dépendances présentes dans
  `app/requirements.txt` et `app/requirements-dev.txt`
- La fonctionnalité doit être testée en local par le développeur
- Si la méthode d'installation et/ou d'exploitation est modifiée suite à un chantier, rédiger
  une nouvelle version des manuels adéquats

## Description des workflows (github action)

### Les workflows dans ce repo

Des github actions ont été conçues pour faciliter la mise en déploiement et le CI/CD plus généralement (voir
.github/workflows).

- [code_quality.yaml](.github/workflows/code_quality.yml): Lance Qodana pour analyser le code
- [deploy_on_prod_back.yml](.github/workflows/deploy_on_prod_back.yml): Déploie la derniere version de main en prod
- [pr_main.yml](.github/workflows/pr_main.yml): Change le nom de la PR au tag actuel de release
- [pr_release.yml](.github/workflows/pr_release.yml):
    - Bump la version en utilisant les labels github "**patch release**", "**minor release**" et  "**majore release**"
    - Pousse l'image docker sur la registry
    - Deploie la nouvelle version sur le VPS de qualification
- [pr_release_check_on_change.yml](.github/workflows/pr_release_check_on_change.yml):
    - Enforce l'utilisation des labels de PR pour le bump de version
    - Change le nom de la PR pour le tag
- [pytest.yml](.github/workflows/pytest.yml): Lance les tests en utilisant pytest

### Note sur les workflows

A l'image d'une application avec ses variables d'environnement, un workflow github utilise des [
_variables_](https://docs.github.com/en/actions/learn-github-actions/variables) et des [
_secrets_](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions).\
Les secrets sont à utiliser à la place des variables quand la valeur est une donnée sensible (ex. une clé API pour un
service payant)

Il est possible de les définir globalement a l'échelle du repository, ou
de [créer des environnements](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment#creating-an-environment)
afin de les regrouper.

Afin d'éditer les variables et les secrets:

- Aller dans `Settings`
- Dans la colonne de gauche, aller dans `Security > Secrets and variables > Actions`

## Création d'une release

### Manuelement

Afin de modifier le numéro de version du projet, il suffit de lancer la commande suivante dans le virtual-env Python
à la racine du projet :

```shell
bumpversion <major|minor|patch>
```

Exemple, pour passer de la version 1.2.3 à la version 1.3.0 :

```shell
bumpversion minor
```

### Avec Github Action (recommandé)

L'opération peut etre effectuée automatiquement grace aux github actions\
Afin de permettre le fonctionnement des actions liées a la creation de releases:

- _(Seulement la première fois)_ Creer les 3 _labels_ suivant dans le repo github en allant à `Issues > Labels`:
    - "**patch release**"
    - "**minor release**"
    - "**major release**"
- Lors de la création de la PR sur release, assigner le label correspondant au type de release.\
  Le workflow [pr_release_check_on_change.yml](.github/workflows/pr_release_check_on_change.yml) sert à vérifier cette
  assignation de label
- Lorsque le merge est validé, le workflow [pr_release.yml](.github/workflows/pr_release.yml) s'occupe du bump, de
  pousser l'image docker sur la registry et du déploiement sur l'environnement de qualification

## Migrations

### À quoi ça sert ?

Après des changements apportés au code de l'ORM (SQLAlchemy), il est très probable que le schema et le contenu de la
base de donnée doive changer (ex. ajout de colonne dans une table)\

- Apres la release **R**, la base de données en production est dans un état **BDD(R)**
- Au moment de la release suivante **R'**, la migration consiste a effectuer les requetes SQL permettant de passer de *
  *BDD(R)** à **BDD(R')**

### Fonctionnement des migrations

Ce projet utilise le package **Flask-Migrate** pour ***faciliter*** les migrations. Plus exactement, **Flask-Migrate**
configure **Alembic**, l'outil de migration de SQLAlchemy, pour marcher correctement avec Flask et Flask-SQLAlchemy\
La procédure ***n'est pas entièrement automatisable*** car il y a une limite aux changements que cet outil peut inférer:

- Alembic n'est pas capable de détecter les changements de noms de table ou de colonnes
- Considérer également le cas où l'on crée une nouvelle colonne _non nullable_: comment Alembic pourrait savoir comment
  la remplir dans la base de donnée actuelle ?

**Flask-Migrate** fonctionne ainsi:

- Une migration est un fichier contenant des operation de creation/modification de la base de données (packages *
  *alembic** et **sqlalchemy**) qui génèrent les requêtes SQL
- Un dossier dédié `migrations` contient la configuration des migrations et l'historique de toutes les migrations
  effectuées (`migrations/versions/*.py`)
- Pour une nouvelle migration, **Flask-Migrate** ***tente*** de génerer le code automatiquement en comparant l'état
  actuel du code et celui de la base de données. Il arrive souvent que cela suffise mais ce n'est pas garanti.
- On verifie le script et le complète éventuellement
- Quand une migration est effectuée, son _revision id_ est automatiquement stocké dans la BDD dans une table
  dédiée `alembic_version`. Cela permet a **Flask-Migrate** de savoir quelles sont les migrations à appliquer

### Utilisation de Flask-Migrate

Depuis le host de la BDD:

- Effectuer un dump de la base de données (adapter la commande aux besoins)\
  `pg_dump -U DB_USER -d DB_NAME -p DB_PORT -C -W nom_du_dump.sql`
- _(En cas de problemes dans la suite)_ Restaurer la BDD a l'aide du dump\
  `pg_restore -U DB_USER -d DB_NAME -p DB_PORT -C -W nom_du_dump.sql`

Depuis le host de l'un des backends:

- Pull la nouvelle release\
  `git pull`
- Lancer l'application:\
  `cd envs/prod && docker compose up flask --build`
- Lancer bash dans le docker:\
  `docker exec -it NOM_DU_SERVICE bash`

Les commandes suivantes sont a lancer dans l'interpréteur bash dans le conteneur.

- _(La premiere fois uniquement)_ Créer le dossier `migrations`:\
  `flask db init`
- _(Optionnel)_ Vérifier que la prochaine migration peut être faite:\
  `flask db check`
- Générer le script de la migration:\
  `flask db migrate -m TAG_DE_LA_RERELEASE`\
  Le tag de release est optionnel mais recommandé, car cela permet de garder trace de la correspondance entre les
  releases et les migrations
- ***Vérifier*** que le script fait bien toutes les bonnes opérations, et le modifier si besoin
- Appliquer la migration:\
  `flask db upgrade`

Commandes utiles:

- `flask db current`: Affiche le _revision id_ actuel de la BDD
- `flask db stamp <revision>`: Change le _revision id_ actuel de la BDD (Attention à ne pas l'utiliser n'importe
  comment !)
- `flask db history`: Affiche, dans l'order chronologique, toutes les migrations effectuées

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
      > **INFO** : sur macos, si les commandes precedentes ne marchent pas executez les commandes suivantes :
      > - ``brew install postgresql``
      > - ``pip install psycopg2-binary ``
        - Si la dépendance sert uniquement à l'environnement de dev ou de CI
            - Toucher à la section [project.optional-dependencies] > dependencies
            - Lancer la commande suivante :
          ```shell
          pip-compile --upgrade --extra=dev --output-file=app/requirements-dev.txt pyproject.toml 
          ```

La commande pip-compile permet de générer les fichiers requirements.txt et requirements-dev.txt, qui contiennent les
dépendances
directes et indirectes et leurs versions figées.

## Workflow des controllers

Le processus de création d'un contrôleur est le suivant :

- Créez un plan (blueprint) qui enregistrera toutes les routes pour ce contrôleur.
- Enregistrez le blueprint à l'application avec app.register_blueprint(...) dans shared/__init__.py
- Pour chaque route :
    - (Optionnel) __Protégez__ la route pour les clients possédant un JWT (supposant que le JWT est utilisé en tant
      ___access token___) en ajoutant le decorateur `@flask_jwt_extended.jwt_required()`
    - (Optionnel) __Obtenez l'identité__ du client en utilisant `flask_jwt_extended.get_jwt_identity()` (supposant que
      le champ 'identity' du JWT ait bien été configuré lors de la création du token)
    - (Routes PUT, POST, PATCH) Recuperer le __payload__ de la requete avec `flask.request.get_json()`
    - Si la requete est triviale, c.a.d. __Create/Read/Update/Delete__:
        - Finir la requete en utilisant la classe utilitaire
          `BaseCRUDHelper`. Les methodes `handle_post/put` s'occuperont de valider les donnees avec le schema fourni au
          constructeur
    - Sinon, la route necessite de la __logique métier__ :
        - Valider les données avec un [schema marshamallow](#schemas)
        - Effaectuer les calculs métiers avec un [service](#services)

## Schemas

Les schemas marshamallow remplissent deux roles en meme temps:

- __Serialisation* / deserialisation__** des donnees
- __Validation__ des donnees

*Sérialisées ->  __Objets Python__\
**Désérialisées ->  __Dictionnaires Python__

### Vocabulaire

Dans marshmallow '__load__' = __deserialize__ et '__dump__' = __serialize__:

__[payload: JSON]__ ----load--->  __[instance: Object]__\
__[payload: JSON]__ <---dump----  __[instance: Object]__

### Definir un schema

- Un schema __marshmallow__ 'pur'

```python3
class Album:
    title: str
    release_date: datetime.date


class AlbumSchema(Schema):
    title = fields.Str()
    release_date = fields.Date()
```

- Un schema __marshmallow_sqlalchemy__

```python3
class AlbumModel:
    title: Column(String(255))
    release_date: Column(Date())


class AlbumSchema(SQLAlchemySchema):
    class Meta:
        model = AlbumModel
        load_instance = True  # Optional: deserialize to model instances
        include_fk = True  # Optional: To include foreign fields
        include_relationships = True  # Optional: To include relationships (become a fields.Related not fields.Nested)

    title = auto_field()
    release_date = auto_field()


# Ou avec SQLAlchemyAutoSchema

class AlbumSchema(SQLAlchemySchema):
    class Meta:
        model = AlbumModel
        load_instance = True  # Optional: deserialize to model instances
        include_fk = True  # Optional: To include foreign fields
        include_relationships = True  # Optional: To include relationships (become a fields.Related not fields.Nested)
```

Note: SQLAlchemySchema n'inclut pas les `sqlalchemy.relationship()`, juste les `sqlalchemy.Column()`

Regarder aussi:

- [marshmallow.fields.Nested()](https://marshmallow.readthedocs.io/en/stable/nesting.html)
- [read_only et dump_only](https://marshmallow.readthedocs.io/en/stable/quickstart.html#read-only-and-write-only-fields)
- [data_key](https://marshmallow.readthedocs.io/en/stable/quickstart.html#specifying-serialization-deserialization-keys)
  pour changer le nom d'un field du dictionnaire en un autre nom dans l'objet

## Services

Les services sont des classes utilitaires regroupant la logique métier propre a une entité\
Leur role est d'encapsuler cette logique (creer des méthodes dont le nom explicite la tache abstrite effectuée) et
donc rendre le code des controllers clair