# Markdown to Text

```
import java.io.File;

public class Md2Txt {

    public static void rename(File file) {
        if (file.isDirectory()) {
            for (File aFile : file.listFiles()) {
                rename(aFile);
            }
        } else {
            renameASingleFile(file);
        }
    }

    public static void renameASingleFile(File file) {
        String fileName = file.getAbsolutePath();
        int spliterIndex = fileName.lastIndexOf(File.separatorChar);
        String path = fileName.substring(0, spliterIndex);
        String name = fileName.substring(spliterIndex + 1);
        if (name.endsWith("md")) {
            String toFile = path + File.separatorChar + name.substring(0, name.lastIndexOf(".")) + ".txt";
            file.renameTo(new File(toFile));
        }
    }

    public static void main(String[] args) {
        rename(new File("tech-wiki"));
    }
}
```
