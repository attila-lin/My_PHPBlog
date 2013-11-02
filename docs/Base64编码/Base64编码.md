# Base64编码

-----

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