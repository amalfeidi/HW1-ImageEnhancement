
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
from skimage.metrics import structural_similarity as ssim


# ==================================================
# 1. Evaluation Metrics
# ==================================================

def calculate_psnr(original, processed):
    return cv2.PSNR(original, processed)


def calculate_ssim(original, processed):
    return ssim(
        original,
        processed,
        channel_axis=2,
        data_range=255
    )


# ==================================================
# 2. Configuration
# ==================================================

IMAGE_FOLDER = "images"

IMAGE_NAMES = [
    "Fog_over_hills.jpg",
    "LOW CONTRAST.jpg",
    "LOW LIGHT.jpg",
    "Shadows of leaves.jpg",
    "Shadows.jpg"
]

# Degradation parameters
alpha = 0.6
beta = 40
sigma = 10

# Gamma correction parameter
gamma = 0.7

# Fixed random seed
rng = np.random.default_rng(42)


# ==================================================
# 3. Output Directories
# ==================================================

DEGRADED_FOLDER = "output/degraded"

LINEAR_FOLDER = "output/enhanced/linear_stretching"

HISTOGRAM_FOLDER = "output/enhanced/histogram_equalization"

GAMMA_FOLDER = "output/enhanced/gamma_correction"

COMPARISON_FOLDER = "output/comparisons"


os.makedirs(DEGRADED_FOLDER, exist_ok=True)
os.makedirs(LINEAR_FOLDER, exist_ok=True)
os.makedirs(HISTOGRAM_FOLDER, exist_ok=True)
os.makedirs(GAMMA_FOLDER, exist_ok=True)
os.makedirs(COMPARISON_FOLDER, exist_ok=True)


# ==================================================
# 4. Lists to Store Images
# ==================================================

original_images = []
reduced_images = []
degraded_images = []

stretched_images = []
equalized_images = []
gamma_images = []

loaded_names = []


# ==================================================
# 5. Resize Images for Display
# ==================================================

def resize_for_display(image, max_width=350):

    height, width = image.shape[:2]

    if width > max_width:

        ratio = max_width / width

        new_width = int(width * ratio)
        new_height = int(height * ratio)

        image = cv2.resize(
            image,
            (new_width, new_height)
        )

    return image


# ==================================================
# 6. Load Images and Generate Degraded Images
# ==================================================

for name in IMAGE_NAMES:

    image_path = os.path.join(IMAGE_FOLDER, name)

    image = cv2.imread(image_path)

    if image is None:

        print(f"Warning: Could not load {name}")
        continue

    print(f"Loaded: {name}, Dimensions: {image.shape}")

    original_images.append(image)
    loaded_names.append(name)

    # Convert image to float
    image_float = image.astype(np.float32)

    # Reduce contrast and add brightness offset
    reduced_image = alpha * image_float + beta

    # Generate Gaussian noise
    noise = rng.normal(
        loc=0,
        scale=sigma,
        size=image.shape
    ).astype(np.float32)

    # Add noise
    noisy_image = reduced_image + noise

    # Clip pixel values to [0, 255]
    reduced_image = np.clip(
        reduced_image, 0, 255
    ).astype(np.uint8)

    degraded_image = np.clip(
        noisy_image, 0, 255
    ).astype(np.uint8)

    reduced_images.append(reduced_image)
    degraded_images.append(degraded_image)

    # Save degraded image
    cv2.imwrite(
        os.path.join(DEGRADED_FOLDER, name),
        degraded_image
    )


# ==================================================
# 7. Linear Contrast Stretching
# ==================================================

for image, name in zip(degraded_images, loaded_names):

    # Convert BGR to LAB
    lab = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2LAB
    )

    L, A, B = cv2.split(lab)

    L_float = L.astype(np.float32)

    # Calculate 2nd and 98th percentiles
    I_min = np.percentile(L_float, 2)
    I_max = np.percentile(L_float, 98)

    if I_max > I_min:

        stretched_L = (
            (L_float - I_min)
            / (I_max - I_min)
        ) * 255

    else:

        stretched_L = L_float

    stretched_L = np.clip(
        stretched_L, 0, 255
    ).astype(np.uint8)

    # Merge LAB channels
    stretched_lab = cv2.merge(
        [stretched_L, A, B]
    )

    # Convert back to BGR
    stretched_image = cv2.cvtColor(
        stretched_lab,
        cv2.COLOR_LAB2BGR
    )

    stretched_images.append(stretched_image)

    cv2.imwrite(
        os.path.join(LINEAR_FOLDER, name),
        stretched_image
    )


# ==================================================
# 8. Histogram Equalization
# ==================================================

for image, name in zip(degraded_images, loaded_names):

    # Convert BGR to LAB
    lab = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2LAB
    )

    L, A, B = cv2.split(lab)

    # Apply histogram equalization to L channel
    equalized_L = cv2.equalizeHist(L)

    # Merge LAB channels
    equalized_lab = cv2.merge(
        [equalized_L, A, B]
    )

    # Convert back to BGR
    equalized_image = cv2.cvtColor(
        equalized_lab,
        cv2.COLOR_LAB2BGR
    )

    equalized_images.append(equalized_image)

    cv2.imwrite(
        os.path.join(HISTOGRAM_FOLDER, name),
        equalized_image
    )


# ==================================================
# 9. Gamma Correction
# ==================================================

for image, name in zip(degraded_images, loaded_names):

    # Convert BGR to LAB
    lab = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2LAB
    )

    L, A, B = cv2.split(lab)

    # Normalize L channel
    L_float = L.astype(np.float32) / 255.0

    # Apply gamma correction
    corrected_L = 255 * (L_float ** gamma)

    corrected_L = np.clip(
        corrected_L, 0, 255
    ).astype(np.uint8)

    # Merge LAB channels
    corrected_lab = cv2.merge(
        [corrected_L, A, B]
    )

    # Convert back to BGR
    gamma_image = cv2.cvtColor(
        corrected_lab,
        cv2.COLOR_LAB2BGR
    )

    gamma_images.append(gamma_image)

    cv2.imwrite(
        os.path.join(GAMMA_FOLDER, name),
        gamma_image
    )


# ==================================================
# 10. Calculate PSNR and SSIM
# ==================================================

metrics = []

for i in range(len(loaded_names)):

    original = original_images[i]
    name = loaded_names[i]

    methods = {
        "Degraded": degraded_images[i],
        "Linear Stretching": stretched_images[i],
        "Histogram Equalization": equalized_images[i],
        "Gamma Correction": gamma_images[i]
    }

    print(f"\nResults for {name}")

    for method_name, processed_image in methods.items():

        psnr_value = calculate_psnr(
            original,
            processed_image
        )

        ssim_value = calculate_ssim(
            original,
            processed_image
        )

        print(
            f"{method_name}: "
            f"PSNR = {psnr_value:.2f} dB, "
            f"SSIM = {ssim_value:.4f}"
        )

        metrics.append([
            name,
            method_name,
            psnr_value,
            ssim_value
        ])


# ==================================================
# 11. Save Metrics to CSV
# ==================================================

csv_path = "output/metrics.csv"

with open(
    csv_path,
    mode="w",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "Image",
        "Method",
        "PSNR (dB)",
        "SSIM"
    ])

    writer.writerows(metrics)

print(f"\nMetrics saved to {csv_path}")


# ==================================================
# 12. Display and Save Visual Comparisons
# ==================================================

for i in range(len(loaded_names)):

    name = loaded_names[i]

    # Convert BGR to RGB for Matplotlib
    original_rgb = cv2.cvtColor(
        original_images[i],
        cv2.COLOR_BGR2RGB
    )

    reduced_rgb = cv2.cvtColor(
        reduced_images[i],
        cv2.COLOR_BGR2RGB
    )

    degraded_rgb = cv2.cvtColor(
        degraded_images[i],
        cv2.COLOR_BGR2RGB
    )

    stretched_rgb = cv2.cvtColor(
        stretched_images[i],
        cv2.COLOR_BGR2RGB
    )

    equalized_rgb = cv2.cvtColor(
        equalized_images[i],
        cv2.COLOR_BGR2RGB
    )

    gamma_rgb = cv2.cvtColor(
        gamma_images[i],
        cv2.COLOR_BGR2RGB
    )

    # Resize images for display
    images_to_show = [
        resize_for_display(original_rgb),
        resize_for_display(reduced_rgb),
        resize_for_display(degraded_rgb),
        resize_for_display(stretched_rgb),
        resize_for_display(equalized_rgb),
        resize_for_display(gamma_rgb)
    ]

    titles = [
        "Original",
        "Reduced Contrast",
        "Degraded",
        "Linear Stretching",
        "Histogram Equalization",
        "Gamma Correction"
    ]

    # Create comparison figure
    plt.figure(figsize=(20, 5))

    for j in range(6):

        plt.subplot(1, 6, j + 1)

        plt.imshow(images_to_show[j])

        plt.title(titles[j], fontsize=9)

        plt.axis("off")

    plt.suptitle(
        name,
        fontsize=14
    )

    plt.tight_layout()

    # Save comparison figure
    comparison_name = (
        name.rsplit(".", 1)[0]
        + "_comparison.png"
    )

    plt.savefig(
        os.path.join(
            COMPARISON_FOLDER,
            comparison_name
        ),
        dpi=300,
        bbox_inches="tight"
    )

    print(
        f"Comparison saved: {comparison_name}"
    )

plt.show()

print("\nAll processing completed successfully!")
