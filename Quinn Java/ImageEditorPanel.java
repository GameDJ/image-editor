import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.File;
import javax.imageio.ImageIO;
import java.awt.*;
import javax.swing.*;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;

@SuppressWarnings("serial")
public class ImageEditorPanel extends JPanel implements MouseListener {

    static BufferedImage imageIn;
    Color[][] imageArray;
    Color[][][] arrayOfImages;
    int width;
    int height;
    int radius = 5;
    double scale = 1;
    boolean flipHorizontal = false;
    boolean flipVertical = false;
    boolean greyscale = false;
    boolean blur = false;
    boolean blurPlus = false;
    boolean blurMinus = false;
    boolean brightness = false;
    boolean brightnessPlus = false;
    boolean brightnessMinus = false;
    boolean undo = false;
    boolean radiusChange = false;
    boolean scaleChange = false;
    int option = 0;

    public ImageEditorPanel() {
        try {
            // the image should be in the main project folder, not in \src or \bin
            imageIn = ImageIO.read(new File("flowers.jpg"));
        } catch (IOException e) {
            System.out.println(e);
        }
        imageArray = makeArray(imageIn);
        height = imageArray.length;
        width = imageArray[0].length;
        System.out.println(width + " x " + height);
        arrayOfImages = new Color[50][imageArray.length][imageArray[0].length];
        setPreferredSize(new Dimension(width + 150, height));
        setBackground(Color.BLACK);
        addMouseListener(this);
    }

    public void paintComponent(Graphics g) {
        // paints the array pixels onto the screen
        arrayOfImages[0] = imageArray;
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                g.setColor(arrayOfImages[option][row][col]);
                g.fillRect(col, row, 1, 1);
            }
        }
        final int CONTROL_BOXES_X = width + 30;
        final int CONTROL_BOXES_Y = 20;
        final int CONTROL_BOXES_WIDTH = 90;
        final int CONTROL_BOXES_HEIGHT = 45;
        final int SPACE_BETWEEN_BOXES = 65;
        final int MINUS_BOX_X = width + 100;
        final int MINUS_BOX_Y = 270;
        final int MINUS_BOX_SIZE = 20;
        final int BRIGHTNESS_BOX_Y = MINUS_BOX_Y + MINUS_BOX_SIZE + 10;
        final int PLUS_BOX_Y = BRIGHTNESS_BOX_Y + 55;
        final int UNDO_BOX_Y = height - 65;
        final int RADIUS_X = width + 70;
        final int RADIUS_Y = 284;
        final int HORIZ_X = width + 36;
        final int HORIZ_Y = 47;
        final int VERT_X = width + 44;
        final int VERT_Y = 111;
        final int GREY_X = width + 47;
        final int GREY_Y = 176;
        final int BLUR_X = width + 62;
        final int BLUR_Y = 241;
        final int PLUS_Y = 285;
        final int MINUS_X = width + 108;
        final int BRIGHT_X = GREY_X - 2;
        final int BRIGHT_Y = RADIUS_Y + 43;
        final int SCALE_X = RADIUS_X - 5;
        final int SCALE_Y = RADIUS_Y + 85;
        final int PLUS_Y2 = BRIGHTNESS_BOX_Y + 70;
        final int MINUS_Y = BRIGHTNESS_BOX_Y + 69;
        final int UNDO_X = width + 58;
        final int UNDO_Y = height - 38;
        final int WHITE_BOX_X1 = width + 65;
        final int WHITE_BOX_Y1 = 272;
        final int WHITE_BOX_SIZE1 = 17;
        final int WHITE_BOX_X2 = SCALE_X - 1;
        final int WHITE_BOX_Y2 = SCALE_Y - 13;
        g.setColor(Color.DARK_GRAY);
        g.fillRect(CONTROL_BOXES_X, CONTROL_BOXES_Y, CONTROL_BOXES_WIDTH, CONTROL_BOXES_HEIGHT);
        g.fillRect(CONTROL_BOXES_X, CONTROL_BOXES_Y + SPACE_BETWEEN_BOXES, CONTROL_BOXES_WIDTH, CONTROL_BOXES_HEIGHT);
        g.fillRect(CONTROL_BOXES_X, CONTROL_BOXES_Y + 2 * SPACE_BETWEEN_BOXES, CONTROL_BOXES_WIDTH,
                CONTROL_BOXES_HEIGHT);
        g.fillRect(CONTROL_BOXES_X, CONTROL_BOXES_Y + 3 * SPACE_BETWEEN_BOXES, CONTROL_BOXES_WIDTH,
                CONTROL_BOXES_HEIGHT);
        g.fillRect(CONTROL_BOXES_X, MINUS_BOX_Y, MINUS_BOX_SIZE, MINUS_BOX_SIZE);
        g.fillRect(MINUS_BOX_X, MINUS_BOX_Y, MINUS_BOX_SIZE, MINUS_BOX_SIZE);
        if (radiusChange) {
            g.setColor(Color.WHITE);
            g.fillRect(WHITE_BOX_X1, WHITE_BOX_Y1, WHITE_BOX_SIZE1, WHITE_BOX_SIZE1);
            radiusChange = false;
            g.setColor(Color.DARK_GRAY);
        }
        g.drawString("" + radius, RADIUS_X, RADIUS_Y);
        g.fillRect(CONTROL_BOXES_X, BRIGHTNESS_BOX_Y, CONTROL_BOXES_WIDTH, CONTROL_BOXES_HEIGHT);
        g.fillRect(CONTROL_BOXES_X, PLUS_BOX_Y, MINUS_BOX_SIZE, MINUS_BOX_SIZE);
        g.fillRect(MINUS_BOX_X, PLUS_BOX_Y, MINUS_BOX_SIZE, MINUS_BOX_SIZE);
        if (scaleChange) {
            g.setColor(Color.WHITE);
            g.fillRect(WHITE_BOX_X2, WHITE_BOX_Y2, MINUS_BOX_SIZE, WHITE_BOX_SIZE1);
            scaleChange = false;
            g.setColor(Color.DARK_GRAY);
        }
        g.drawString("" + scale, SCALE_X, SCALE_Y);
        g.fillRect(CONTROL_BOXES_X, UNDO_BOX_Y, CONTROL_BOXES_WIDTH, CONTROL_BOXES_HEIGHT);
        g.setColor(Color.WHITE);
        g.drawString("Flip Horizontal", HORIZ_X, HORIZ_Y);
        g.drawString("Flip Vertical", VERT_X, VERT_Y);
        g.drawString("Greyscale", GREY_X, GREY_Y);
        g.drawString("Blur", BLUR_X, BLUR_Y);
        g.drawString("+", HORIZ_X, PLUS_Y);
        g.drawString("-", MINUS_X, RADIUS_Y);
        g.drawString("Brightness", BRIGHT_X, BRIGHT_Y);
        g.drawString("+", HORIZ_X, PLUS_Y2);
        g.drawString("-", MINUS_X, MINUS_Y);
        g.drawString("Undo", UNDO_X, UNDO_Y);
    }

    public void run() {
        // call your image-processing methods here OR call them from keyboard event handling methods
        // write image-processing methods as pure functions - for example: array = flip(array);
        if (flipHorizontal) {
            option++;
            arrayOfImages[option] = flipHorizontal(arrayOfImages[option - 1]);
            flipHorizontal = false;
        }
        if (flipVertical) {
            option++;
            arrayOfImages[option] = flipVertical(arrayOfImages[option - 1]);
            flipVertical = false;
        }
        if (greyscale) {
            option++;
            arrayOfImages[option] = greyscale(arrayOfImages[option - 1]);
            greyscale = false;
        }
        if (blur) {
            option++;
            arrayOfImages[option] = blur(arrayOfImages[option - 1], radius);
            blur = false;
        }
        if (blurPlus) {
            radius++;
            radiusChange = true;
            blurPlus = false;
        }
        if (blurMinus) {
            radius--;
            radiusChange = true;
            blurMinus = false;
        }
        if (brightness) {
            option++;
            arrayOfImages[option] = brightness(arrayOfImages[option - 1], scale);
            brightness = false;
        }
        if (brightnessPlus) {
            scale += 0.1;
            scaleChange = true;
            brightnessPlus = false;
        }
        if (brightnessMinus) {
            scale -= 0.1;
            scaleChange = true;
            brightnessMinus = false;
        }
        if (undo) {
            option--;
            if (option < 0) option = 0;
            flipHorizontal = false;
            flipVertical = false;
            greyscale = false;
            blur = false;
            undo = false;
        }
        repaint();
    }

    public Color[][] makeArray(BufferedImage image) {
        int width = image.getWidth();
        int height = image.getHeight();
        Color[][] result = new Color[height][width];
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                Color c = new Color(image.getRGB(col, row), true);
                result[row][col] = c;
            }
        }
        System.out.println(width + " x " + height);
        return result;
    }

    public Color[][] flipHorizontal(Color[][] input) {
        int height = input.length;
        int width = input[0].length;
        Color[][] output = new Color[height][width];
        int lastColumnElement = input[0].length - 1;
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                output[row][lastColumnElement - col] = input[row][col];
            }
        }
        return output;
    }

    public Color[][] flipVertical(Color[][] input) {
        int height = input.length;
        int width = input[0].length;
        Color[][] output = new Color[height][width];
        int lastRowElement = input.length - 1;
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                output[lastRowElement - row][col] = input[row][col];
            }
        }
        return output;
    }

    public Color[][] greyscale(Color[][] input) {
        int height = input.length;
        int width = input[0].length;
        Color[][] output = new Color[height][width];
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                int red = input[row][col].getRed();
                int green = input[row][col].getGreen();
                int blue = input[row][col].getBlue();
                int average = (red + green + blue) / 3;
                output[row][col] = new Color(average, average, average);
            }
        }
        return output;
    }

    public Color[][] blur(Color[][] input, int radius) {
        int height = input.length;
        int width = input[0].length;
        Color[][] output = new Color[height][width];
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                int red = 0;
                int green = 0;
                int blue = 0;
                int k = 0;
                for (int i = row - radius; i <= row + radius; i++) {
                    for (int j = col - radius; j <= col + radius; j++) {
                        if (isOnScreen(i, j)) {
                            red += input[i][j].getRed();
                            green += input[i][j].getGreen();
                            blue += input[i][j].getBlue();
                            k++;
                        }
                    }
                }
                red /= k;
                green /= k;
                blue /= k;
                output[row][col] = new Color(red, green, blue);
            }
        }
        return output;
    }

    public boolean isOnScreen(int i, int j) {
        if (i < 0 || j < 0)
            return false;
        if (i >= height || j >= width)
            return false;
        return true;
    }

    public Color[][] brightness(Color[][] input, double scale) {
        int height = input.length;
        int width = input[0].length;
        Color[][] output = new Color[height][width];
        for (int row = 0; row < height; row++) {
            for (int col = 0; col < width; col++) {
                int red = (int) (input[row][col].getRed() * scale);
                int green = (int) (input[row][col].getGreen() * scale);
                int blue = (int) (input[row][col].getBlue() * scale);
                if (red > 255) red = 255;
                if (red < 0) red = 0;
                if (green > 255) green = 255;
                if (green < 0) green = 0;
                if (blue > 255) blue = 255;
                if (blue < 0) blue = 0;
                output[row][col] = new Color(red, green, blue);
            }
        }
        return output;
    }

    public void mouseClicked(MouseEvent e) {
        // called when the mouse is pressed and released quickly
    }

    public void mouseEntered(MouseEvent e) {
        // called when the mouse enters the window
    }

    public void mouseExited(MouseEvent e) {
        // called when the mouse leaves the window
    }

    public void mousePressed(MouseEvent e) {
        int pressX = e.getX();
        int pressY = e.getY();
        // set a variable based on mouse coordinates
        // or check a condition based on mouse coordinates
        final int CONTROL_BOXES_X = width + 30;
        final int CONTROL_BOXES_Y = 20;
        final int CONTROL_BOXES_WIDTH = 90;
        final int CONTROL_BOXES_HEIGHT = 45;
        final int SPACE_BETWEEN_BOXES = 65;
        final int MINUS_BOX_X = width + 100;
        final int MINUS_BOX_Y = 270;
        final int MINUS_BOX_SIZE = 20;
        final int UNDO_BOX_Y = height - 65;
        final int BRIGHTNESS_BOX_Y = MINUS_BOX_Y + MINUS_BOX_SIZE + 10;
        final int PLUS_BOX_Y = BRIGHTNESS_BOX_Y + 55;
        if (pressX >= CONTROL_BOXES_X && pressX <= CONTROL_BOXES_X + CONTROL_BOXES_WIDTH && pressY >= CONTROL_BOXES_Y
                && pressY <= SPACE_BETWEEN_BOXES) {
            flipHorizontal = true;
        }
        if (pressX >= CONTROL_BOXES_X && pressX <= CONTROL_BOXES_X + CONTROL_BOXES_WIDTH
                && pressY >= CONTROL_BOXES_Y + SPACE_BETWEEN_BOXES && pressY <= 2 * SPACE_BETWEEN_BOXES) {
            flipVertical = true;
        }
        if (pressX >= CONTROL_BOXES_X && pressX <= CONTROL_BOXES_X + CONTROL_BOXES_WIDTH
                && pressY >= CONTROL_BOXES_Y + 2 * SPACE_BETWEEN_BOXES && pressY <= 3 * SPACE_BETWEEN_BOXES) {
            greyscale = true;
        }
        if (pressX >= CONTROL_BOXES_X && pressX <= CONTROL_BOXES_X + CONTROL_BOXES_WIDTH
                && pressY >= CONTROL_BOXES_Y + 3 * SPACE_BETWEEN_BOXES && pressY <= 4 * SPACE_BETWEEN_BOXES) {
            blur = true;
        }
        if (pressX >= CONTROL_BOXES_X && pressX <= CONTROL_BOXES_X + CONTROL_BOXES_WIDTH && pressY >= UNDO_BOX_Y
                && pressY <= UNDO_BOX_Y + CONTROL_BOXES_HEIGHT) {
            undo = true;
        }
        if (pressX >= CONTROL_BOXES_X && pressX <= CONTROL_BOXES_X + MINUS_BOX_SIZE && pressY >= MINUS_BOX_Y
                && pressY <= MINUS_BOX_Y + MINUS_BOX_SIZE) {
            blurPlus = true;
        }
        if (pressX >= MINUS_BOX_X && pressX <= CONTROL_BOXES_X + CONTROL_BOXES_WIDTH && pressY >= MINUS_BOX_Y
                && pressY <= MINUS_BOX_Y + MINUS_BOX_SIZE) {
            blurMinus = true;
        }
        if (pressX >= CONTROL_BOXES_X && pressX <= CONTROL_BOXES_X + CONTROL_BOXES_WIDTH && pressY >= BRIGHTNESS_BOX_Y
                && pressY <= BRIGHTNESS_BOX_Y + CONTROL_BOXES_HEIGHT) {
            brightness = true;
        }
        if (pressX >= CONTROL_BOXES_X && pressX <= CONTROL_BOXES_X + MINUS_BOX_SIZE && pressY >= PLUS_BOX_Y
                && pressY <= PLUS_BOX_Y + MINUS_BOX_SIZE) {
            brightnessPlus = true;
        }
        if (pressX >= MINUS_BOX_X && pressX <= MINUS_BOX_X + MINUS_BOX_SIZE && pressY >= PLUS_BOX_Y
                && pressY <= PLUS_BOX_Y + MINUS_BOX_SIZE) {
            brightnessMinus = true;
        }
        run();
    }

    public void mouseReleased(MouseEvent e) {
        int releaseX = e.getX();
        int releaseY = e.getY();
        // set a variable based on mouse coordinates
        // or check a condition based on mouse coordinates
    }
}