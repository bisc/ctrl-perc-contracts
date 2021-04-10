import java.io.PrintWriter;

import prism.PrismException;
//import PRISMConnectorAPI

public class runWaterTankintBaseline {

	
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runWaterTankintBaseline () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		
		String waterTankFolder = "/data2/mcleav/waterTankEx/singleTankEx/";
		String propsFile = "/data2/mcleav/waterTankEx/singleTankEx/intBaselineProps.props";
		// String propsFile = "/data2/mcleav/waterTankEx/singleTankEx/tankProps.props";
		
				
        String myModelName = "intBaselineSingleTank.prism";
        // String myModelName = "trimmedBaselineSingleTank.prism";
        // String myModelName = "singleTankSameAsintBaselineTesting.prism";
        String myModel = waterTankFolder + myModelName;
        
        String mypolicy = "";
        String consts = "wlidInit=13";
        
        PrismConnectorAPI pc= new PrismConnectorAPI();
        
        
        final long startTime = System.nanoTime();
        String res = pc.modelCheckFromFileS(myModel,propsFile, mypolicy, consts);
        long durationTime = (System.nanoTime() - startTime);
        pc.close();
        double ans = Double.parseDouble(res);
        System.out.println(ans);
        System.out.println((durationTime)/(1000000));
			
			
    }
}

