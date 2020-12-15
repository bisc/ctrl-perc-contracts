import java.io.PrintWriter;

import prism.PrismException;
//import PRISMConnectorAPI

public class conservativeExp1 {

	
	PrismConnectorAPI myPrismConnectorAPI;
	
	public conservativeExp1 () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		
		String baselineFolder = "/data2/mcleav/latticeScalability/baselineModels/exactBaseline/";
		String propsFile = "/data2/mcleav/latticeScalability/propsForJava.props";

		int[] initDistanceValues = {100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,195,200};
		int[] initSpeedValues = {10,14,18,22,26};

        double deltaD = 0.5;

		double[][] crashProbs = new double[initDistanceValues.length][initSpeedValues.length];
		double[][] crashProbsDeltad = new double[initDistanceValues.length][initSpeedValues.length];

		for(int i=0;i<initDistanceValues.length;i++) {
			for(int j=0;j<initSpeedValues.length;j++) {
				int initDist = initDistanceValues[i];
				int initSpeed = initSpeedValues[j];
				
				String myModelName = "lecBaselineMajVoteFilterH3L3DistDisc0.04.prism";
				String myModel = baselineFolder + myModelName;
				
				double distDisc = 0.04;
				double speedDisc = 0.4;
				String mypolicy = "";
				initDist1 = (int) Math.round(initDist/distDisc);
				initSpeed1 = (int) Math.round(initSpeed/speedDisc);

                initDist2 = (int) Math.round((initDist+deltaD)/distDisc);
				initSpeed2 = (int) Math.round(initSpeed/speedDisc);

        		String consts1 = "initPos=" + (initDist1) + ",initSpeed=" + (initSpeed1) + ",initBrakingFlag=0,initBraking=1,carPosThresh=" + (int) Math.round(5/distDisc);
        		String consts2 = "initPos=" + (initDist2) + ",initSpeed=" + (initSpeed2) + ",initBrakingFlag=0,initBraking=1,carPosThresh=" + (int) Math.round(5/distDisc);

				System.out.println(consts1);
				PrismConnectorAPI pc= new PrismConnectorAPI();
				
				
		        String res1 = pc.modelCheckFromFileS(myModel,propsFile, mypolicy, consts1);

		        String res2 = pc.modelCheckFromFileS(myModel,propsFile, mypolicy, consts2);

		        pc.close();
		        double ans1 = Double.parseDouble(res1);
		        double ans2 = Double.parseDouble(res2);

		        crashProbs[i][j] = ans1;
                crashProbsDeltad[i][j] = ans2;

				System.out.println(initDist);
				System.out.println(initSpeed);
				System.out.println((int) Math.round(5/distDisc));
		        
			}
		}
		
		String resultsFolder = "/data2/mcleav/latticeScalability/results/";
		
        String runTimeResults = resultsFolder + "extraPointsrunTimesExactBaseline.csv";
        PrintWriter runTimeWriter = new PrintWriter(runTimeResults);
        
        String crashProbResults = resultsFolder + "extraPointscrashProbsExactBaseline.csv";
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
