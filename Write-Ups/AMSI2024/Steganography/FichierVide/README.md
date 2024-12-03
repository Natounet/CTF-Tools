
# Analysis and Flag Extraction Using Whitespace and ReverseFUCK

## 1. Whitespace

The challenge name, "Empty file," gives us a significant clue.  
This is likely a "Whitespace" code—a form of steganography that hides information using spaces and tabulations.

Using the online decoder at [dcode.fr](https://www.dcode.fr/whitespace-language), we retrieve the following:

```
----------]<-<---<-------<---------->>>>+[<<<+++++,------------,------,++++++++++,<-----------------------,++++++++++++++,>------------,<+,--------,>>-------------------,<<++++,++++,>>--,<----------,------,<--,>++,>+++,<-,>-,<<,>---,<-----,----------, 
```

## 2. A Strange Code

The extracted string resembles Brainfuck code. However, decoding it as Brainfuck (via [dcode.fr](https://www.dcode.fr/brainfuck-language)) results in an error.  
This is because the code is written in a variant called "ReverseFUCK."

Using the ReverseFUCK decoder at [dcode.fr](https://www.dcode.fr/reversefuck-language), we retrieve the flag:

```
AMSI{mUlt1pl3_enc0d1ngs}
```

## 3. The Flag

The flag extracted is:
```
AMSI{mUlt1pl3_enc0d1ngs}
```
