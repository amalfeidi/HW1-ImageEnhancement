# Image Enhancement – Computer Vision Homework 1

## 1. Project Description

This project focuses on implementing and comparing classical image enhancement techniques using Python, OpenCV, and NumPy.

Five real colour images were selected to represent different visual conditions:

- Fog and low visibility
- Low contrast
- Low illumination
- Non-uniform shadows

The objective is to improve image appearance and evaluate the performance of different enhancement methods using objective quality metrics and visual inspection.

## 2. Technologies and Libraries

The project uses:

- Python 3.11.9
- OpenCV
- NumPy
- Matplotlib
- Scikit-image

## 3. Dataset

Five original images are used:

1. `Fog_over_hills.jpg`
2. `LOW CONTRAST.jpg`
3. `LOW LIGHT.jpg`
4. `Shadows of leaves.jpg`
5. `Shadows.jpg`

All original images are stored in the `images/` directory.

## 4. Image Degradation

To simulate degraded image conditions, contrast reduction, a brightness offset, and Gaussian noise are applied to the original images.

The degradation model is:

\[
I_d = \operatorname{clip}(\alpha I + \beta + N, 0, 255)
\]

Where:

- \(I\): Original image
- \(I_d\): Degraded image
- \(\alpha\): Contrast reduction factor
- \(\beta\): Brightness offset
- \(N\): Gaussian noise

The parameters used are:

| Parameter | Value |
|---|---:|
| Contrast factor (\(\alpha\)) | 0.6 |
| Brightness offset (\(\beta\)) | 40 |
| Noise mean | 0 |
| Noise standard deviation (\(\sigma\)) | 10 |
| Random seed | 42 |

The degradation process is applied independently to the three colour channels. Pixel values are clipped to the range [0, 255].

A fixed random seed ensures reproducibility of noise generation.

## 5. Image Enhancement Methods

Three classical image enhancement techniques are implemented.

### 5.1 Linear Contrast Stretching

Linear Contrast Stretching expands the intensity range to improve image contrast.

The method is applied to the L (Lightness) channel in LAB colour space, while the A and B channels remain unchanged.

The 2nd and 98th percentiles are used to calculate the intensity range, reducing the influence of extreme pixel values.

### 5.2 Histogram Equalization

Histogram Equalization improves global contrast by redistributing intensity values.

The method is applied using OpenCV's `cv2.equalizeHist()` function on the L channel in LAB colour space. The A and B channels are preserved.

### 5.3 Gamma Correction

Gamma Correction adjusts image brightness using a nonlinear transformation:

\[
I_{out}=255\left(\frac{I_{in}}{255}\right)^\gamma
\]

The selected gamma value is:

```python
gamma = 0.7
```

The correction is applied to the L channel in LAB colour space.

## 6. Image Quality Evaluation

The processed images are compared with their corresponding original images using two quality metrics.

### 6.1 PSNR (Peak Signal-to-Noise Ratio)

PSNR measures pixel-level differences between two images. Higher values indicate greater similarity in pixel intensities.

### 6.2 SSIM (Structural Similarity Index)

SSIM measures structural similarity between two images, considering luminance, contrast, and structure. Values closer to 1 indicate greater structural similarity.

Both metrics are calculated for:

- Degraded images
- Linear Contrast Stretching
- Histogram Equalization
- Gamma Correction

This produces 20 image-condition evaluations in total (5 images × 4 conditions).

The results are saved in:

```text
output/metrics.csv
```

## 7. Project Structure

```text
HW1_ImageEnhancement/
│
├── images/
│   ├── Fog_over_hills.jpg
│   ├── LOW CONTRAST.jpg
│   ├── LOW LIGHT.jpg
│   ├── Shadows of leaves.jpg
│   └── Shadows.jpg
│
├── output/
│   ├── degraded/
│   ├── enhanced/
│   │   ├── linear_stretching/
│   │   ├── histogram_equalization/
│   │   └── gamma_correction/
│   │
│   ├── comparisons/
│   └── metrics.csv
│
├── src/
│   └── main.py
│
├── README.md
└── requirements.txt
```

The output directories are created automatically when the program runs.

## 8. Installation

Make sure Python 3.11.9 is installed.

Install the required libraries using:

```bash
pip install -r requirements.txt
```

Alternatively, install them individually:

```bash
pip install opencv-python numpy matplotlib scikit-image
```

## 9. How to Run

Open a terminal in the project root directory and execute:

```bash
python src/main.py
```

The program automatically:

1. Loads the five original images.
2. Generates degraded versions.
3. Applies the three enhancement methods.
4. Saves the enhanced images.
5. Calculates PSNR and SSIM.
6. Exports the evaluation results to a CSV file.
7. Generates and saves visual comparison figures.

## 10. Reproducibility

A fixed random seed is used:

```python
rng = np.random.default_rng(42)
```

This ensures reproducible Gaussian noise generation when the same input images and parameters are used.

The degradation parameters are documented in the source code and in this README.

## 11. Image Sources and Licenses

The original images were obtained from Wikimedia Commons and Unsplash.

1. **Fog over hills:** Jon Sullivan – Public Domain.  
   [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Fog_over_hills.jpg)

2. **Low contrast:** Marcin Kolodziejczak – Unsplash License.  
   [Original image](https://unsplash.com/fr/photos/foret-brumeuse-avec-des-arbres-anciens-et-noueux-et-de-lherbe-verte-yF--zAzHJg8)

3. **Low light:** Paolo Chiabrando – Unsplash License.  
   [Original image](https://unsplash.com/fr/photos/une-piece-sombre-avec-une-lumiere-venant-par-une-fenetre-dMGV2jJShdo)

4. **Shadows of leaves:** Tomwsulcer – CC0.  
   [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Shadows_of_leaves_on_a_wall.jpg)

5. **Shadows:** Compo – CC BY-SA 4.0.  
   [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Shadows_on_vertical_blinds.jpg)

The original authors and applicable licenses are acknowledged.

## 12. Conclusion

The experiments demonstrate that image enhancement performance depends on the characteristics of the input image.

Linear Contrast Stretching provided good results for several images, while Histogram Equalization sometimes amplified noise and produced excessive brightness.

Gamma Correction provided moderate brightness improvements in some cases.

The results also demonstrate that numerical metrics and visual inspection should be considered together when evaluating image enhancement quality.

## 13. Repository

The complete project, including source code, original images, processed images, comparison figures, and evaluation metrics, is available on GitHub:

[HW1 – Image Enhancement Repository](https://github.com/amalfeidi/HW1-ImageEnhancement)