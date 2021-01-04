import java.io.PrintWriter;

import prism.PrismException;
//import PRISMConnectorAPI

public class testExactBaseline {

	
	PrismConnectorAPI myPrismConnectorAPI;
	
	public testExactBaseline () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		
		String baselineFolder = "/data2/mcleav/latticeScalability/baselineModels/exactBaseline/";
		//String propsFile = "/data2/mcleav/latticeScalability/propsForJavaTestExactBaselineSpeed.props";
		String propsFile = "/data2/mcleav/latticeScalability/propsForJava.props";
		
		int[] initDistanceValues = {166};
		int[] initSpeedValues = {20};

		double[][] runTimes = new double[initDistanceValues.length][initSpeedValues.length];
		double[][] crashProbs = new double[initDistanceValues.length][initSpeedValues.length];
		
		for(int i=0;i<initDistanceValues.length;i++) {
			for(int j=0;j<initSpeedValues.length;j++) {
				//int initDist = initDistanceValues[i];
				//int initSpeed = initSpeedValues[j];

				double initDist = 166;
				double initSpeed = 20;
				
				String myModelName = "lecBaselineMajVoteFilterH3L3DistDisc0.04.prism";
				String myModel = baselineFolder + myModelName;
				
				double distDisc = 0.04;
				double speedDisc = 0.4;
				String mypolicy = "";
                //double nextDistVal = (((double) initDist)-(1*((double) initSpeed)/10));
				double nextDistVal = 5;
				double nextSpeedVal = ((double) initSpeed - 1*0.4);
				int initDist1 = (int) Math.round(initDist/distDisc);
				int initSpeed1 = (int) Math.round(initSpeed/speedDisc);
        		String consts = "initPos=" + (initDist1) + ",initSpeed=" + (initSpeed1) + ",initBrakingFlag=0,initBraking=1,carPosThresh=" + (int) (Math.round(nextDistVal/distDisc));
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
