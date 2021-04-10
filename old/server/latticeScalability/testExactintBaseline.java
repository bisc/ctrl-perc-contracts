import java.io.PrintWriter;

import prism.PrismException;
//import PRISMConnectorAPI

public class testExactintBaseline {

	
	PrismConnectorAPI myPrismConnectorAPI;
	
	public testExactintBaseline () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		
		String baselineFolder = "/data2/mcleav/latticeScalability/intModels/";
		//String propsFile = "/data2/mcleav/latticeScalability/propsForJavaTestExactBaselineSpeed.props";
		String propsFile = "/data2/mcleav/latticeScalability/propsForintBaselines.props";
		
		int[] initDistanceValues = {120};
		int[] initSpeedValues = {26};

		double[][] runTimes = new double[initDistanceValues.length][initSpeedValues.length];
		double[][] crashProbs = new double[initDistanceValues.length][initSpeedValues.length];
		
		for(int i=0;i<initDistanceValues.length;i++) {
			for(int j=0;j<initSpeedValues.length;j++) {
				//int initDist = initDistanceValues[i];
				//int initSpeed = initSpeedValues[j];

				double initDist = 120;
				double initSpeed = 26;
				
				//String myModelName = "intBaselineAEBSConstLECInitCond1NoRoundingOnePoint0.250000.prism";
                //String myModelName = "intBaselineAEBSConstLECInitCond1NoRounding0.040000.prism";
				//String myModelName = "intBaselineAEBS_initd120.000000_initv26.000000.prism";
				String myModelName = "intBaselineAEBSConstLECInitCond1NoRoundingTrimmed0.250000.prism";
				String myModel = baselineFolder + myModelName;
				
				double distDisc = 0.25;
				double speedDisc = 0.4;
				String mypolicy = "";
                //double nextDistVal = (((double) initDist)-(1*((double) initSpeed)/10));
				double nextDistVal = 5;
				double nextSpeedVal = ((double) initSpeed - 1*0.4);
				int initDist1 = (int) Math.round(initDist/distDisc)+1;
				int initSpeed1 = (int) Math.round(initSpeed/speedDisc)+1;
        		String consts = "didMax=" + (initDist1) + ",vidMax=" + (initSpeed1);
				//(int) (Math.round(initSpeed/speedDisc))
				System.out.println(consts);
				PrismConnectorAPI pc= new PrismConnectorAPI();
				
				
		        final long startTime = System.nanoTime();
		        String res = pc.modelCheckFromFileS(myModel,propsFile, mypolicy, consts);
		        final long durationTime = System.nanoTime() - startTime;
		        pc.close();
		        double ans = Double.parseDouble(res);
		        
		        runTimes[i][j] = durationTime;
		        crashProbs[i][j] = ans;

				System.out.println(initDist);
				System.out.println(initSpeed);
				System.out.println(nextDistVal);
				System.out.println(nextSpeedVal);
				System.out.println((Math.round(nextSpeedVal/speedDisc)));
				System.out.println((int) (Math.round(nextSpeedVal/speedDisc)));
		        
			}
		}
	}
		
}
