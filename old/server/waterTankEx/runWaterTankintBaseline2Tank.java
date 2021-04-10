import java.io.PrintWriter;

import prism.PrismException;
//import PRISMConnectorAPI

public class runWaterTankintBaseline2Tank {

	
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runWaterTankintBaseline2Tank () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		
		String waterTankFolder = "/data2/mcleav/waterTankEx/doubleTankEx/";
		String propsFile = "/data2/mcleav/waterTankEx/doubleTankEx/intBaselineProps.props";
        // String propsFile = "/data2/mcleav/waterTankEx/doubleTankEx/intBaselinePropsDebug.props";
		// String propsFile = "/data2/mcleav/waterTankEx/singleTankEx/tankProps.props";
		
        // String myModelName = "testModel2Tankint_2.prism";
        // String myModelName = "testModel2TankTrimmed_2_2.prism";
        // String consts = "wlidInit1=25,wlidInit2=25,initContAction1=0,initContAction2=0";

        // String myModelName = "testModel2TankTrimmed_2_3.prism";
        // String myModelName = "testModel2TankBaseline_3.prism";
        // String consts = "wlidInit1=17,wlidInit2=17,initContAction1=0,initContAction2=0";

        // String myModelName = "testModel2TankTrimmed_2_4.prism";
        // String myModelName = "testModel2TankBaseline_5.prism";
        // String consts = "wlidInit1=13,wlidInit2=13,initContAction1=0,initContAction2=0";

        // String myModelName = "testModel2TankTrimmed_2_5.prism";
        // String myModelName = "testModel2TankBaseline_5.prism";
        // String consts = "wlidInit1=10,wlidInit2=10,initContAction1=0,initContAction2=0";

        // String myModelName = "testModel2TankTrimmed_2_6.prism";
        // String myModelName = "testModel2TankBaseline_5.prism";
        // String consts = "wlidInit1=9,wlidInit2=9,initContAction1=0,initContAction2=0";

        // String myModelName = "testModel2TankTrimmed_2_7.prism";
        // String myModelName = "testModel2TankBaseline_5.prism";
        // String consts = "wlidInit1=8,wlidInit2=8,initContAction1=0,initContAction2=0";


        // String myModelName = "testModel2TankTrimmed_2_8.prism";
        // String myModelName = "testModel2TankBaseline_5.prism";
        // String consts = "wlidInit1=13,wlidInit2=13,initContAction1=0,initContAction2=0";

        // String myModelName = "testModel2TankTrimmed_2_10.prism";
        // String myModelName = "testModel2TankBaseline_5.prism";
        // String consts = "wlidInit1=5,wlidInit2=5,initContAction1=0,initContAction2=0";

        // String myModelName = "testModel2TankBaseline.prism";
        String myModelName = "testModel2TankBaseline_1.prism";
        // String myModelName = "testModel2TankBaseline_2.prism";
        // String myModelName = "testModel2TankBaseline_3.prism";
        String consts = "wlidInit1=50,wlidInit2=50,initContAction1=0,initContAction2=0";

        // String myModelName = "twoTankintBaseline_trimmed.prism";
        // String myModelName = "singleTankSameAsintBaselineTesting.prism";
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

