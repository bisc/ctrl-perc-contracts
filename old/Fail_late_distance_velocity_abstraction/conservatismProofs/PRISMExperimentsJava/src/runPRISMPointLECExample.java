
import prism.PrismException;

import org.jzy3d

public class runPRISMPointLECExample {
	
	PrismConnectorAPI myPrismConnectorAPI;
	
	
	public runPRISMPointLECExample () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	
	public static void main (String[] args) throws Exception {
		int distLower = 0;
		int distUpper = 5000;
		int speedLower = 0;
		int speedUpper = 6000;
		
		int distDisc = 2000;
		int speedDisc = 3000;
		
        String res="result";
        //String myModel = "/Users/jcamara/Dropbox/Documents/Work/Projects/BRASS/rainbow-prototype/trunk/rainbow-brass/prismtmp/0.prism";
        String myModel = "C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\conservatismProofs\\PRISMExperiments\\smoothLEC\\PointLECsimpleAnalysis.prism";
        //String myPolicy = "/Users/jcamara/Dropbox/Documents/Work/Projects/BRASS/rainbow-prototype/trunk/rainbow-brass/prismtmp/0";
        String myPolicy = "Unused";
        //String myProps = "/Users/jcamara/Dropbox/Documents/Work/Projects/BRASS/rainbow-prototype/trunk/rainbow-brass/prismtmp/mapbot.props";
        String myProps = "C:\\Users\\matth\\Documents\\Penn\\safetyContract\\lattice\\conservatismProofs\\PRISMExperiments\\smoothLEC\\propsForJava.props";

        int numDistPoints = 1+(distUpper-distLower)/distDisc;
        int numSpeedPoints = 1+(speedUpper-speedLower)/speedDisc;
        double[][] safetyArray = new double[numDistPoints][numSpeedPoints];
		for (int dist = 0; dist<numDistPoints; dist+=1) {
			for (int speed = 0; speed<numSpeedPoints; speed+=1) {
		        String consts = "initPos=" + (dist*distDisc-distLower) + ",initSpeed=" + (speed*speedDisc-speedLower);
		        System.out.println(consts);
		        PrismConnectorAPI pc= new PrismConnectorAPI();
//				res = pc.modelCheckFromFileS(myModel,"R{\"time\"}min=? [ F goal ]", myPolicy);
		        res = pc.modelCheckFromFileS(myModel,myProps, myPolicy, consts);
		        double ans = Double.parseDouble(res);
		        safetyArray[dist][speed] = ans;
			}
		}
		System.out.println(safetyArray);
		
	}
}


