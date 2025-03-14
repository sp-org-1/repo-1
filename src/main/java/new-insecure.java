import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;

import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

//import org.apache.commons.io.FileUtils;

import com.fasterxml.jackson.databind.ObjectMapper;

public class Insecure {

  public void badFunction(HttpServletRequest request) throws IOException {
    String obj = request.getParameter("data");
    ObjectMapper mapper = new ObjectMapper();
    mapper.enableDefaultTyping();
    String val = mapper.readValue(obj, String.class);
    File tempDir;
    tempDir = File.createTempFile("", ".");
    tempDir.delete();
    tempDir.mkdir();
    Files.exists(Paths.get("/tmp/", obj));
  }

  //public void test1() {
  //  String img = FileUtils.getInstance().getUserImagePath(request.getRemoteUser()) + extension;
  //  final ByteArrayResource inputStream  new ByteArrayResource(fileCache.getFileBytes(img));
  //}
}
