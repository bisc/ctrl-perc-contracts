import java.io.PrintWriter;

import prism.PrismException;
//import PRISMConnectorAPI

public class runWaterTankCoseqModel {

	
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runWaterTankCoseqModel () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		
		String waterTankFolder = "/data2/mcleav/waterTankEx/conseqLECModel/";
		// String propsFile = "/data2/mcleav/waterTankEx/doubleTankEx/intBaselineProps.props";
        String propsFile = "/data2/mcleav/waterTankEx/conseqLECModel/testProps.props";
        // String myModelName = "simpleModelEnd.prism";
        String myModelName = "simpleModelEndSimData.prism";
        String consts = "wlInit1=50,wlInit2=50,initContAction1=0,initContAction2=0";
        // String consts = "wlInit1=30,wlInit2=70,initContAction1=0,initContAction2=0";

        String myModel = waterTankFolder + myModelName;
        
        String mypolicy = "";
        // String consts = "wlidInit1=50,wlidInit2=50,initContAction1=0,initContAction2=0";
        
        PrismConnectorAPI pc= new PrismConnectorAPI();
        
        
        final long startTime = System.nanoTime();
        String res = pc.modelCheckFromFileS(myModel,propsFile, mypolicy, consts);
        long durationTime = (System.nanoTime() - startTime);
        pc.close();
        double ans = Double.parseDouble(res);
        System.out.println(myModelName);
        System.out.println(ans);
        System.out.println((double) (durationTime)/(1000000000));
			
			
    }
}

