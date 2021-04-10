import java.io.PrintWriter;

import prism.PrismException;
//import PRISMConnectorAPI

public class runWaterTank2ExForEMSOFT {

	
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runWaterTank2ExForEMSOFT () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		
		String waterTankFolder = "/data2/mcleav/waterTankEx/doubleTankEx/";
        String propsFile = "/data2/mcleav/waterTankEx/doubleTankEx/tankPropsSink.props";
        String myModelName = "twoTanksEx.prism";
        String myModel = waterTankFolder + myModelName;
        String mypolicy = "";

		// int[] initWaterLevels1 = {20,50,90};
        int[] initWaterLevels1 = {20,50};
		// int[] initWaterLevels2 = {1,2,37,49};
        // int[] initWaterLevels1 = {10,20,30,40,50,60,70,80,90};

		double[][] runTimes = new double[initWaterLevels1.length][initWaterLevels1.length];
		double[][] crashProbs = new double[initWaterLevels1.length][initWaterLevels1.length];
		
		int cont1State = 0;
		int cont2State = 0;

		for(int i=0;i<initWaterLevels1.length;i++) {

			for(int j=0;j<initWaterLevels1.length;j++) {
				
                int tempInitWaterLevel1 = (int) initWaterLevels1[i];
				int tempInitWaterLevel2 = (int) initWaterLevels1[j];

                String consts = "wl1Init=" + (tempInitWaterLevel1) + ",wl2Init=" + (tempInitWaterLevel2) + ",cont1State=" + (cont1State) + ",cont2State=" + (cont2State);
                
                System.out.println(consts);
                PrismConnectorAPI pc= new PrismConnectorAPI();
                
                
                final long startTime = System.nanoTime();
                String res = pc.modelCheckFromFileS(myModel,propsFile, mypolicy, consts);
                long durationTime = (System.nanoTime() - startTime);
                pc.close();
                double ans = Double.parseDouble(res);

                runTimes[i][j] = durationTime;
				crashProbs[i][j] = ans;


                System.out.println(myModelName);
                System.out.println(ans);
                System.out.println((double) (durationTime)/(1000000000));
                    

            }
        }

		String resultsFolder = "/data2/mcleav/waterTankEx/EMSOFTResults/";
		
        String runTimeResults = resultsFolder + "runTimesTwoTankBaseline.csv";
        PrintWriter runTimeWriter = new PrintWriter(runTimeResults);
        
        String crashProbResults = resultsFolder + "crashProbsTwoTankBaseline.csv";
        PrintWriter crashProbsWriter = new PrintWriter(crashProbResults);
        for(int i=0;i<initWaterLevels1.length;i++) {
			for(int j=0;j<initWaterLevels1.length;j++) {
				double tempRunTime = runTimes[i][j];
				double tempCrashProb = crashProbs[i][j];
				if(j==initWaterLevels1.length-1) {
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

