# Image Enhancement Project

## 1. Project Description

This project focuses on implementing and comparing image enhancement techniques using Python and OpenCV.

Five real color images were selected to represent different image conditions:

- Fog and low visibility
- Low contrast
- Low illumination
- Non-uniform shadows

The objective is to improve image appearance and evaluate the performance of different enhancement methods using objective quality metrics and visual inspection.

## 2. Technologies and Libraries

The project uses:

- Python
- OpenCV
- NumPy
- Matplotlib
- Scikit-image

## 3. Dataset

Five original images are used:

1. Fog_over_hills.jpg
2. LOW CONTRAST.jpg
3. LOW LIGHT.jpg
4. Shadows of leaves.jpg
5. Shadows.jpg

The original images are stored in the `images/` directory.

## 4. Image Degradation

To simulate degraded image conditions, contrast reduction and Gaussian noise are applied to the original images.

The degradation process is:

\[
I_d = \alpha I + \beta + N
\]

Where:

- \(I\): Original image
- \(\alpha\): Contrast reduction factor
- \(\beta\): Brightness offset
- \(N\): Gaussian noise

The parameters used are:

| Parameter | Value |
|---|---:|
| Alpha | 0.6 |
| Beta | 40 |
| Noise mean | 0 |
| Noise standard deviation | 10 |
| Random seed | 42 |

Pixel values are clipped to the range [0, 255].

A fixed random seed ensures reproducibility of the noise generation.

## 5. Image Enhancement Methods

Three image enhancement techniques are implemented.

### 5.1 Linear Contrast Stretching

Linear Contrast Stretching expands the intensity range to improve image contrast.

The method is applied to the L (Lightness) channel in LAB color space.

The 2nd and 98th percentiles are used to calculate the intensity range, reducing the influence of extreme pixel values.

### 5.2 Histogram Equalization

Histogram Equalization improves global contrast by redistributing intensity values.

The method is applied using OpenCV's `equalizeHist()` function on the L channel in LAB color space.

### 5.3 Gamma Correction

Gamma Correction adjusts image brightness using a nonlinear transformation.

The transformation is:

\[
I_{out}=255\left(\frac{I_{in}}{255}\right)^\gamma
\]

The selected gamma value is:

```python
gamma = 0.7
```

The correction is applied to the L channel in LAB color space.

## 6. Image Quality Evaluation

The processed images are compared with their corresponding original images using two quality metrics.

### 6.1 PSNR (Peak Signal-to-Noise Ratio)

PSNR measures pixel-level differences between two images.

Higher PSNR values indicate greater similarity in pixel intensities.

### 6.2 SSIM (Structural Similarity Index)

SSIM measures structural similarity between two images, considering luminance, contrast, and structure.

Values closer to 1 indicate greater structural similarity.

Both metrics are calculated for:

- Degraded images
- Linear Contrast Stretching
- Histogram Equalization
- Gamma Correction

This produces 20 image-method comparisons in total.

The results are saved in:

```text
output/metrics.csv
```

## 7. Project Structure

```text
HW1_ImageEnhancement/
│
├── images/
│
├── output/
│   ├── degraded/
│   │
│   ├── enhanced/
│   │   ├── linear_stretching/
│   │   ├── histogram_equalization/
│   │   └── gamma_correction/
│   │
│   └── metrics.csv
│
├── src/
│   └── main.py
│
└── README.md
```

## 8. Installation

Install the required Python libraries:

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
7. Displays visual comparisons.

## 10. Reproducibility

A fixed random seed is used:

```python
rng = np.random.default_rng(42)
```

This ensures reproducible Gaussian noise generation when the same input images and parameters are used.

## 11. Conclusion

The experiments demonstrate that image enhancement performance depends on the characteristics of the input image.

Linear Contrast Stretching provided good results for several images, while Histogram Equalization sometimes amplified noise and produced excessive brightness.

Gamma Correction provided moderate brightness enhancement in some cases.

The results also demonstrate that numerical metrics and visual inspection should be considered together when evaluating image enhancement techniques.

## 12. Image Sources and Licenses

The original images and their sources should be documented here.

For each image, provide its source URL and license information, where available.