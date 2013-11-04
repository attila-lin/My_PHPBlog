Base64编码
========

Base64是一种基于64个可打印字符来表示二进制数据的表示方法。由于2的6次方等于64，所以每6个位元为一个单元，对应某个可打印字符。三个字节有24个位元，对应于4个Base64单元，即3个字节需要用4个可打印字符来表示。它可用来作为电子邮件的传输编码。在Base64中的可打印字符包括字母A-Z、a-z、数字0-9，这样共有62个字符，此外两个可打印符号在不同的系统中而不同。一些如uuencode的其他编码方法，和之后binhex的版本使用不同的64字符集来代表6个二进制数字，但是它们不叫Base64。
Base64常用于在通常处理文本数据的场合，表示、传输、存储一些二进制数据。包括MIME的email，email via MIME,在XML中存储复杂数据.


舉例來說，一段引用自托马斯·霍布斯的利维坦的文句：

> Man is distinguished, not only by his reason, but by this singular passion from other animals, which is a lust of the mind, that by a perseverance of delight in the continued and indefatigable generation of knowledge, exceeds the short vehemence of any carnal pleasure.

經過base64編碼之後變成：

>TWFuIGlzIGRpc3Rpbmd1aXNoZWQsIG5vdCBvbmx5IGJ5IGhpcyByZWFzb24sIGJ1dCBieSB0aGlz
>IHNpbmd1bGFyIHBhc3Npb24gZnJvbSBvdGhlciBhbmltYWxzLCB3aGljaCBpcyBhIGx1c3Qgb2Yg
>dGhlIG1pbmQsIHRoYXQgYnkgYSBwZXJzZXZlcmFuY2Ugb2YgZGVsaWdodCBpbiB0aGUgY29udGlu
>dWVkIGFuZCBpbmRlZmF0aWdhYmxlIGdlbmVyYXRpb24gb2Yga25vd2xlZGdlLCBleGNlZWRzIHRo
>ZSBzaG9ydCB2ZWhlbWVuY2Ugb2YgYW55IGNhcm5hbCBwbGVhc3VyZS4=

    import java.io.*;  
    import java.util.*;
    
    
    /*
    主要复习各种转换 = =||||
    http://community.topcoder.com/tc?module=ProjectDetail&pj=30029043&tab=results
    */
    
    
    public class Base64{
    	public static String getpasswd(String str){
        		char[] chars = str.toCharArray();  
        		//System.out.println(str.length());
        		StringBuffer sbu = new StringBuffer();
    
    		for(int i = 0 ; i < chars.length; i ++){
    			int z = Integer.parseInt( Integer.toBinaryString((int)chars[i]) );
    			String k = String.format("%08d", z );
    			//System.out.println(k);
    			sbu.append( k );
    		}
    
    		String temp = sbu.toString();
    		//System.out.println(temp);
    		String result = "";
    		String heh = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+//";
    		for(int i = 0; i < temp.length(); i+=6){
    			Integer ints = Integer.valueOf( temp.substring(i, i+6),2) ;
    			//System.out.println(  ints.intValue()  );
    			//System.out.println(   heh.charAt(ints.intValue())  );
    			result += heh.charAt(ints.intValue()) ;
    		}
    		//System.out.println(result);
    		return result;
    	}
    
    	public static void main(String[] args){
    		System.out.print("Enter your file:");
    		
    		Scanner sc  = new Scanner(System.in);
    		String input  = sc.next();
    
    		try{//创建文件输入流对象  
    			String output = null;
    			StringBuffer sb = new StringBuffer();
    			FileInputStream rf = new FileInputStream(input);
    			BufferedReader br = new BufferedReader(new InputStreamReader(rf)); 
    			while ((output = br.readLine()) != null) {
    				sb.append(output);
    			}
    			output = sb.toString();
    			//System.out.println(output.length());
    			String result = getpasswd(output);
    			System.out.println(result);
    			rf.close();//关闭输入流
    		}
    		catch(Exception e){
    			System.out.println(e);
    		}
    	}
    }