from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay


# ============================================================
# 1. Configuration
# ============================================================

SEED = 42
IMAGE_SIZE = (28, 28)
BATCH_SIZE = 32
EPOCHS = 15

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DIR = BASE_DIR / "knowledge"
TEST_DIR = BASE_DIR / "tests"

MODEL_PATH = BASE_DIR / "modele_formes.keras"

CLASS_NAMES = ["cercle", "rectangle", "triangle"]

tf.keras.utils.set_random_seed(SEED)


# ============================================================
# 2. Chargement et prétraitement des images
# ============================================================

def preprocess_image(image_path):
    """
    Charge une image, la convertit en niveaux de gris,
    la redimensionne et normalise ses pixels entre 0 et 1.
    """

    with Image.open(image_path) as image:
        image = image.convert("L")
        image = image.resize(IMAGE_SIZE)

        image_array = np.asarray(image, dtype=np.float32) / 255.0

    # Ajout du canal correspondant à l'image en niveaux de gris.
    return image_array[..., np.newaxis]

def explore_images():
    """Affiche quelques images originales et leurs caractéristiques."""

    print("\nEXPLORATION DES IMAGES ORIGINALES")

    for class_name in CLASS_NAMES:
        image_path = next(
            (KNOWLEDGE_DIR / class_name).glob("*.png")
        )

        with Image.open(image_path) as image:
            print(
                f"{image_path.name} : "
                f"dimensions={image.size}, "
                f"mode={image.mode}, "
                f"format={image.format}"
            )

            plt.figure(figsize=(3, 3))
            plt.imshow(image)
            plt.title(class_name)
            plt.axis("off")
            plt.show()
            plt.close()

def load_training_images():
    """Charge les images classées dans les dossiers knowledge."""

    images = []
    labels = []

    for label, class_name in enumerate(CLASS_NAMES):
        class_dir = KNOWLEDGE_DIR / class_name

        if not class_dir.exists():
            raise FileNotFoundError(
                f"Dossier introuvable : {class_dir}"
            )

        image_paths = sorted(class_dir.glob("*.png"))

        if not image_paths:
            raise ValueError(
                f"Aucune image trouvée dans {class_dir}"
            )

        for image_path in image_paths:
            images.append(preprocess_image(image_path))
            labels.append(label)

        print(
            f"Classe {class_name} : "
            f"{len(image_paths)} images chargées."
        )

    X = np.asarray(images, dtype=np.float32)
    y = np.asarray(labels, dtype=np.int32)

    return X, y


# ============================================================
# 3. Séparation des données
# ============================================================

def split_data(X, y):
    """
    Sépare les données en :
    - 70 % pour l'entraînement ;
    - 15 % pour la validation ;
    - 15 % pour le test interne.
    """

    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=SEED,
        stratify=y,
    )

    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        random_state=SEED,
        stratify=y_temp,
    )

    print("\nRépartition des données :")
    print(f"Entraînement : {len(X_train)} images")
    print(f"Validation   : {len(X_val)} images")
    print(f"Test interne : {len(X_test)} images")

    return X_train, X_val, X_test, y_train, y_val, y_test


# ============================================================
# 4. Création du réseau de neurones
# ============================================================

def create_model():
    """Construit un réseau de neurones convolutif (CNN)."""

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(28, 28, 1)),

        tf.keras.layers.Conv2D(
            16,
            kernel_size=3,
            activation="relu",
            padding="same",
        ),
        tf.keras.layers.MaxPooling2D(pool_size=2),

        tf.keras.layers.Conv2D(
            32,
            kernel_size=3,
            activation="relu",
            padding="same",
        ),
        tf.keras.layers.MaxPooling2D(pool_size=2),

        tf.keras.layers.Flatten(),

        tf.keras.layers.Dense(64, activation="relu"),

        # Trois probabilités : cercle, rectangle et triangle.
        tf.keras.layers.Dense(3, activation="softmax"),
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


# ============================================================
# 5. Visualisation de l'entraînement
# ============================================================

def plot_training_history(history):
    """Enregistre les courbes de précision et de perte."""

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    axes[0].plot(history.history["accuracy"], label="Entraînement")
    axes[0].plot(history.history["val_accuracy"], label="Validation")
    axes[0].set_title("Précision du modèle")
    axes[0].set_xlabel("Époque")
    axes[0].set_ylabel("Accuracy")
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(history.history["loss"], label="Entraînement")
    axes[1].plot(history.history["val_loss"], label="Validation")
    axes[1].set_title("Perte du modèle")
    axes[1].set_xlabel("Époque")
    axes[1].set_ylabel("Loss")
    axes[1].legend()
    axes[1].grid(True)

    fig.tight_layout()
    fig.savefig(BASE_DIR / "courbes_entrainement.png")
    plt.close(fig)


# ============================================================
# 6. Évaluation sur le test interne
# ============================================================

def evaluate_model(model, X_test, y_test):
    """Évalue le modèle sur les images mises de côté."""

    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)

    print("\n" + "=" * 55)
    print("ÉVALUATION SUR LE TEST INTERNE")
    print("=" * 55)
    print(f"Loss     : {loss:.4f}")
    print(f"Accuracy : {accuracy:.2%}")

    predictions = np.argmax(model.predict(X_test, verbose=0), axis=1)

    print("\nRapport de classification :")
    print(
        classification_report(
            y_test,
            predictions,
            labels=[0, 1, 2],
            target_names=CLASS_NAMES,
            zero_division=0,
        )
    )

    matrix = confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1, 2],
    )

    display = ConfusionMatrixDisplay(
        confusion_matrix=matrix,
        display_labels=CLASS_NAMES,
    )

    display.plot(cmap="Blues", values_format="d")
    plt.title("Matrice de confusion - Test interne")
    plt.tight_layout()
    plt.savefig(BASE_DIR / "matrice_confusion.png")
    plt.close()

    return loss, accuracy


# ============================================================
# 7. Prédiction sur les 60 images du dossier tests
# ============================================================

def evaluate_external_images(model):
    """
    Évalue les images générées par generateImgTest.py.

    Le script fourni crée les images dans cet ordre :
    0 à 19  : cercles
    20 à 39 : rectangles
    40 à 59 : triangles
    """

    if not TEST_DIR.exists():
        print("\nDossier tests introuvable : évaluation ignorée.")
        return

    image_paths = list(TEST_DIR.glob("*.png"))

    # Tri numérique : test2.png doit précéder test10.png.
    image_paths.sort(
        key=lambda path: int(path.stem.replace("test", ""))
    )

    if not image_paths:
        print("\nAucune image trouvée dans tests/.")
        return

    if len(image_paths) != 60:
        print(
            f"\nAttention : {len(image_paths)} images trouvées "
            "au lieu des 60 attendues."
        )

    X_external = np.asarray(
        [preprocess_image(path) for path in image_paths],
        dtype=np.float32,
    )

    probabilities = model.predict(X_external, verbose=0)
    predicted_labels = np.argmax(probabilities, axis=1)

    print("\n" + "=" * 55)
    print("PRÉDICTIONS SUR LES IMAGES DU DOSSIER tests/")
    print("=" * 55)

    for path, prediction, scores in zip(
        image_paths, predicted_labels, probabilities
    ):
        print(
            f"\n{path.name} -> {CLASS_NAMES[prediction]}"
        )

        for class_name, score in zip(CLASS_NAMES, scores):
            print(f"  {class_name}: {score:.2%}")

    # Les étiquettes réelles sont connues grâce à l'ordre
    # de génération défini dans generateImgTest.py.
    if len(image_paths) == 60:
        y_external = np.repeat([0, 1, 2], 20)

        external_accuracy = np.mean(
            predicted_labels == y_external
        )

        print("\nRésultat sur les 60 images externes :")
        print(f"Accuracy : {external_accuracy:.2%}")

        print("\nRapport de classification externe :")
        print(
            classification_report(
                y_external,
                predicted_labels,
                labels=[0, 1, 2],
                target_names=CLASS_NAMES,
                zero_division=0,
            )
        )


# ============================================================
# 8. Exécution principale
# ============================================================

def main():
    print("=" * 55)
    print("CLASSIFICATION D'IMAGES DE FORMES GÉOMÉTRIQUES")
    print("=" * 55)

    explore_images()

    X, y = load_training_images()

    print(f"\nDimensions des images : {X.shape}")
    print(f"Dimensions des étiquettes : {y.shape}")

    (
        X_train,
        X_val,
        X_test,
        y_train,
        y_val,
        y_test,
    ) = split_data(X, y)

    model = create_model()

    print("\nArchitecture du modèle :")
    model.summary()

    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True,
    )

    print("\nDébut de l'entraînement...")

    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        callbacks=[early_stopping],
        verbose=1,
    )

    plot_training_history(history)

    loss, accuracy = evaluate_model(
        model,
        X_test,
        y_test,
    )

    model.save(MODEL_PATH)
    print(f"\nModèle sauvegardé : {MODEL_PATH}")

    evaluate_external_images(model)

    print("\nFichiers générés :")
    print("- modele_formes.keras")
    print("- courbes_entrainement.png")
    print("- matrice_confusion.png")

    print("\nFin du programme.")


if __name__ == "__main__":
    main()