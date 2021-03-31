# Handwritten

For those who are too lazy to write lectures by hand. My own handwritten font is used here. Distance learning has dramatically increased the number of lectures that had to be written by hand. So I wrote this small program.

## Example

Here is an example in English (left) and in Russian (right). English isn't my native language, so I write like a robot :)

<img src="https://github.com/xcapt0/handwritten/blob/master/docs/assets/example-en.jpg?raw=true" alt="drawing" width="400"/><img src="https://github.com/xcapt0/handwritten/blob/master/docs/assets/example-ru.jpg?raw=true" alt="drawing" width="400"/>

In Russian looks more real, at least the lecturer didn't notice.

## Getting started

### Install project

```
pip install handwritten-image
```

### Simple Example

```python
from handwritten_image import HandWrite
hand = HandWrite()
hand.convert_to_image('your-text-file.docx', random_select=False)
```

## Convert to a handwritten images

You can easily convert your text to handwritten text using this method

```python
hand.convert_to_image('your-text-file.docx') # or .doc and .txt file
```

### Save directory

Specify the folder where you want to save the images using `save_dir` argument, if not specified, they will be saved to the current folder

```python
hand.convert_to_image('your-text-file.docx', save_dir='images')
```

### Random selection

If you don't need random sampling from the text, you can specify `random_select=False` argument

```python
hand.convert_to_image('your-text-file.docx', random_select=False)
```

## Text file to edit

Before converting to images, you may want to change the text (add brackets, remove extra characters, etc.). If `edit=True` it creates a txt file that you can edit and then use to create images.

```python
hand.to_txt('your-text-file.docx', edit=True) # or .doc and .txt file
```

**Note**
> Before converting the file to an image, remove the **`hand.to_txt()`** call, otherwise it will overwrite the file you edited

After you edit the file, you can convert this file

```python
hand.convert_to_image('your-edited-file.txt', random_select=False)
```

### Random selection

You also can specify the `random_select=False` argument if you don't need a random selection

```python
hand.to_txt('your-text-file.docx', random_select=False)
```

### Save folder

Default folder to save in your script folder and default file name is `temp.txt`. Specify `save_path` argument **with** file type if you want to change the name

```python
hand.to_txt('your-text-file.docx', save_path='your-folder/file.txt')
```
