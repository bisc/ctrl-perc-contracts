package PRISMExperimentsJavaMaven.erhts;

import java.io.PrintWriter;

import prism.PrismException;

public class runAEBSBaselineWindowDiffDistDiscs {
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runAEBSBaselineWindowDiffDistDiscs () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		int initDist = 1660;
		//int initDist = 75;
		int initSpeed = 200;
		
        String res="result";
        
        
        PrismConnectorAPI pc= new PrismConnectorAPI();
        // Longer Stateful LEC Model from Carla Data
        String myModelArbCondWindowed = "C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\conservatismProofs\\PRISMExperiments\\smoothLEC\\PointLECAEBSAnalysisLECModelFromCarlaDataArbCondLECWindowed.prism";
        
        String myPolicyArbCondWindowed = "Unused";
        String myPropsArbCondWindowed = "C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\conservatismProofs\\PRISMExperiments\\smoothLEC\\propsForJava.props";

        String constsArbCondWindowed = "initPos=" + (initDist) + ",initSpeed=" + (initSpeed)+ ",initBrakingFlag=0,initBraking=1";
        //PrismConnectorAPI pc= new PrismConnectorAPI();

        final long startTimeArbCondWindowed = System.nanoTime();
        res = pc.modelCheckFromFileS(myModelArbCondWindowed,myPropsArbCondWindowed, myPolicyArbCondWindowed, constsArbCondWindowed);
        final long durationArbCondWindowed = System.nanoTime() - startTimeArbCondWindowed;
        pc.close();
        double ansArbCondWindowed = Double.parseDouble(res);
        
        
        System.out.println("Done Running PRISM");
        
        /*System.out.println(duration/1000000000);
        System.out.println(ans);

        System.out.println(durationCond/1000000000);
        System.out.println(ansCond);
        
        System.out.println(durationArbCond/1000000000);
        System.out.println(ansArbCond);*/
        
        System.out.println(durationArbCondWindowed/1000000000);
        System.out.println(ansArbCondWindowed);
	}

}
