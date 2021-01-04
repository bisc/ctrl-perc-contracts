import java.io.PrintWriter;

import prism.PrismException;
//import PRISMConnectorAPI

public class runScalabilityRamneetKandN {

	
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runScalabilityRamneetKandN () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		
		String m = "3";
		String latticeFolder = "/data2/mcleav/latticeScalability/ramneetKandNModels/m" + m + "/";
		
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

				/*if(initDist>=165 && initSpeed==26) {
					if(initDist != 200) {
						runTimes[i][j]=0;
						crashProbs[i][j] = 1;
						continue;
					}
				}
				if(initDist==100 && initSpeed==26){
					runTimes[i][j] = 0;
					crashProbs[i][j] = 1;
					continue;
				}*/
				
				String myModelName = "pos" + initDist + "0.0_v" + initSpeed + "0.0.prism";
				String propsName = "pos" + initDist + "0.0_v" + initSpeed + "0.0.props";
				String myModel = latticeFolder + myModelName;
				String myProps = latticeFolder + propsName;
				
				System.out.println(myModel);
				String mypolicy = "";
				String consts = "";
				
				PrismConnectorAPI pc= new PrismConnectorAPI();
				
				
		        final long startTime = System.nanoTime();
		        String res = pc.modelCheckFromFileS(myModel,myProps, mypolicy, consts);
		        final long durationTime = System.nanoTime() - startTime;
		        pc.close();
		        double ans = Double.parseDouble(res);
		        
		        runTimes[i][j] = durationTime;
		        crashProbs[i][j] = ans;
		        
			}
		}
		
		String resultsFolder = "/data2/mcleav/latticeScalability/results/";
		
        String runTimeResults = resultsFolder + "extraPointsrunTimesRamneetKandNm" + m + ".csv";
        PrintWriter runTimeWriter = new PrintWriter(runTimeResults);
        
        String crashProbResults = resultsFolder + "extraPointscrashProbsRamneetKandNm" + m + ".csv";
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
