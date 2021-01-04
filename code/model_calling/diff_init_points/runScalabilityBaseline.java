import java.io.PrintWriter;

import prism.PrismException;
//import PRISMConnectorAPI

public class runScalabilityBaseline {

	
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runScalabilityBaseline () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		
		String baselineFolder = "/data2/mcleav/latticeScalability/baselineModels/";
		String propsFile = "/data2/mcleav/latticeScalability/propsForJava.props";
		
		//int[] initDistanceValues = {120,130,140,150,160,170,180};
		//int[] initSpeedValues = {10,14,18,22,26,30};
		
		//int[] initDistanceValues = {120,125,130,135,140};
		//int[] initSpeedValues = {10,14,18,22,26};

		int[] initDistanceValues = {100,105,110,115,145,150,155,160,165,170,175,180,185,190,195,200};
		int[] initSpeedValues = {10,14,18,22,26};

		//int[] initDistanceValues = {120,125};
		//int[] initSpeedValues = {10,12};
		double[][] runTimes = new double[initDistanceValues.length][initSpeedValues.length];
		double[][] crashProbs = new double[initDistanceValues.length][initSpeedValues.length];
		
		for(int i=0;i<initDistanceValues.length;i++) {
			for(int j=0;j<initSpeedValues.length;j++) {
				int initDist = initDistanceValues[i];
				int initSpeed = initSpeedValues[j];
				
				String myModelName = "lecBaselineMajVoteFilterH3L3DistDisc0.25.prism";
				String myModel = baselineFolder + myModelName;
				
				double distDisc = 0.25;
				double speedDisc = 0.1;
				String mypolicy = "";
				initDist = (int) Math.round(initDist/distDisc);
				initSpeed = (int) Math.round(initSpeed/speedDisc);
        		String consts = "initPos=" + (initDist) + ",initSpeed=" + (initSpeed) + ",initBrakingFlag=0,initBraking=1,carPosThresh=" + (int) Math.round(5/distDisc);
				
				System.out.println(consts);
				PrismConnectorAPI pc= new PrismConnectorAPI();
				
				
		        final long startTime = System.nanoTime();
		        String res = pc.modelCheckFromFileS(myModel,propsFile, mypolicy, consts);
		        final long durationTime = System.nanoTime() - startTime;
		        pc.close();
		        double ans = Double.parseDouble(res);
		        
		        runTimes[i][j] = durationTime;
		        crashProbs[i][j] = ans;
		        
			}
		}
		
		String resultsFolder = "/data2/mcleav/latticeScalability/results/";
		
        String runTimeResults = resultsFolder + "extraPointsrunTimesBaseline.csv";
        PrintWriter runTimeWriter = new PrintWriter(runTimeResults);
        
        String crashProbResults = resultsFolder + "extraPointscrashProbsBaseline.csv";
        PrintWriter crashProbsWriter = new PrintWriter(crashProbResults);
        for(int i=0;i<initDistanceValues.length;i++) {
        	for(int j=0; j<initSpeedValues.length;j++) {
        		double tempRunTime = runTimes[i][j];
        		double tempCrashProb = crashProbs[i][j];
        		if(j==initSpeedValues.length-1) {
        			runTimeWriter.print(tempRunTime);
        			crashProbsWriter.print(tempCrashProb);
        		}
        		else {
        			runTimeWriter.print(tempRunTime + ",");
        			crashProbsWriter.print(tempCrashProb + ",");
        		}
        	}
        	runTimeWriter.println("");
        	crashProbsWriter.println("");
        }
        
        runTimeWriter.close();
        crashProbsWriter.close();
	}
		
}
