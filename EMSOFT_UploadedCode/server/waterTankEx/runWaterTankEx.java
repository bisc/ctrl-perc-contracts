import java.io.PrintWriter;

import prism.PrismException;
//import PRISMConnectorAPI

public class runWaterTankEx {

	
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runWaterTankEx () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		
		String waterTankFolder = "/data2/mcleav/waterTankEx/singleTankEx/";
		String propsFile = "/data2/mcleav/waterTankEx/singleTankEx/tankProps.props";
		
		// int[] initWaterLevels = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50};
		int[] initWaterLevels = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49};
		// int[] initWaterLevels = {1,2,7,25,37,49};

		double[] runTimes = new double[initWaterLevels.length];
		double[] crashProbs = new double[initWaterLevels.length];
		
		for(int i=0;i<initWaterLevels.length;i++) {
				
			String myModelName = "singleTankSimple2.prism";
			String myModel = waterTankFolder + myModelName;
			
			int tempInitWaterLevel = (int) initWaterLevels[i];
			int tempInitCont = 7;
			String mypolicy = "";
			String consts = "wlInit=" + (tempInitWaterLevel) + ",initCont=" + (tempInitCont);
			System.out.println(consts);
			
			PrismConnectorAPI pc= new PrismConnectorAPI();
			
			
			final long startTime = System.nanoTime();
			String res = pc.modelCheckFromFileS(myModel,propsFile, mypolicy, consts);
			final long durationTime = System.nanoTime() - startTime;
			pc.close();
			double ans = Double.parseDouble(res);
			
			runTimes[i] = durationTime;
			crashProbs[i] = ans;
			
		}
		
		String resultsFolder = "/data2/mcleav/waterTankEx/singleTankEx/";
		
        String runTimeResults = resultsFolder + "runTimesBadPerception_initCont1.csv";
        PrintWriter runTimeWriter = new PrintWriter(runTimeResults);
        
        String crashProbResults = resultsFolder + "crashProbsBadPerception_initCont1.csv";
        PrintWriter crashProbsWriter = new PrintWriter(crashProbResults);
        for(int i=0;i<initWaterLevels.length;i++) {
			double tempRunTime = runTimes[i];
			double tempCrashProb = crashProbs[i];
			if(i==initWaterLevels.length-1) {
				runTimeWriter.print(tempRunTime);
				crashProbsWriter.print(tempCrashProb);
			}
			else {
				runTimeWriter.print(tempRunTime + ",");
				crashProbsWriter.print(tempCrashProb + ",");
			}
        }
        
        runTimeWriter.close();
        crashProbsWriter.close();
	}
		
}
