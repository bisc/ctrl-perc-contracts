import java.io.PrintWriter;

import prism.PrismException;
//import PRISMConnectorAPI

public class runWaterTank2Ex {

	
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runWaterTank2Ex () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		
		String waterTankFolder = "/data2/mcleav/waterTankEx/doubleTankEx/";
		String propsFile = "/data2/mcleav/waterTankEx/doubleTankEx/tankPropsSink.props";
		
		// int[] initWaterLevels1 = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50};
		// int[] initWaterLevels1 = {0,5,10,15,20,25,30,35,40,45,50};
		// int[] initWaterLevels2 = {0,5,10,15,20,25,30,35,40,45,50}
		// int[] initWaterLevels1 = {1,3,5,10,15,20,25,30,35,40,45,47,49};
		int[] initWaterLevels1 = {50};
		// int[] initWaterLevels2 = {1,2,37,49};


		double[][] runTimes = new double[initWaterLevels1.length][initWaterLevels1.length];
		double[][] crashProbs = new double[initWaterLevels1.length][initWaterLevels1.length];
		
		int cont1State = 0;
		int cont2State = 0;

		for(int i=0;i<initWaterLevels1.length;i++) {

			for(int j=0;j<=i;j++) {
				
				String myModelName = "twoTanksEx.prism";
				String myModel = waterTankFolder + myModelName;
				
				int tempInitWaterLevel1 = (int) initWaterLevels1[i];
				int tempInitWaterLevel2 = (int) initWaterLevels1[j];
				String mypolicy = "";
				String consts = "wl1Init=" + (tempInitWaterLevel1) + ",wl2Init=" + (tempInitWaterLevel2) + ",cont1State=" + (cont1State) + ",cont2State=" + (cont2State);
				System.out.println(consts);
				
				PrismConnectorAPI pc= new PrismConnectorAPI();
				
				
				final long startTime = System.nanoTime();
				String res = pc.modelCheckFromFileS(myModel,propsFile, mypolicy, consts);
				final long durationTime = System.nanoTime() - startTime;
				pc.close();
				double ans = Double.parseDouble(res);
				
				runTimes[i][j] = durationTime;
				crashProbs[i][j] = ans;

				runTimes[j][i] = durationTime;
				crashProbs[j][i] = ans;

				System.out.println(ans);
				System.out.println((double) (durationTime)/(1000000000));
			}
			
		}
		
		// String resultsFolder = "/data2/mcleav/waterTankEx/doubleTankEx/";
		
        // String runTimeResults = resultsFolder + "runTimesTwoTankTest.csv";
        // PrintWriter runTimeWriter = new PrintWriter(runTimeResults);
        
        // String crashProbResults = resultsFolder + "crashProbsTwoTankTest.csv";
        // PrintWriter crashProbsWriter = new PrintWriter(crashProbResults);
        // for(int i=0;i<initWaterLevels1.length;i++) {
		// 	for(int j=0;j<=i;j++) {
		// 		double tempRunTime = runTimes[i][j];
		// 		double tempCrashProb = crashProbs[i][j];
		// 		if(j==i) {
		// 			runTimeWriter.print(tempRunTime);
		// 			crashProbsWriter.print(tempCrashProb);
		// 		}
		// 		else {
		// 			runTimeWriter.print(tempRunTime + ",");
		// 			crashProbsWriter.print(tempCrashProb + ",");
		// 		}
		// 	}
		// 	runTimeWriter.println("");
        // 	crashProbsWriter.println("");
        // }
        
        // runTimeWriter.close();
        // crashProbsWriter.close();
	}
		
}
