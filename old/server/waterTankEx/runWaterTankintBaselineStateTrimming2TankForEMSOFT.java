import java.io.PrintWriter;

import prism.PrismException;
//import PRISMConnectorAPI

public class runWaterTankintBaselineStateTrimming2TankForEMSOFT {

	
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runWaterTankintBaselineStateTrimming2TankForEMSOFT () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		
		String waterTankFolder = "/data2/mcleav/waterTankEx/doubleTankExStateTrimming/";
        String propsFile = "/data2/mcleav/waterTankEx/doubleTankExStateTrimming/intBaselineProps.props";
        String myModelName = "testModel2TankTrimmed_2_4_simLEC.prism";
        String myModel = waterTankFolder + myModelName;
        String mypolicy = "";

		// int[] initWaterLevels1 = {20,50,90};
		// int[] initWaterLevels2 = {1,2,37,49};
        int[] initWaterLevels1 = {10,20,30,40,50,60,70,80,90};

		double[][] runTimes = new double[initWaterLevels1.length][initWaterLevels1.length];
		double[][] crashProbs = new double[initWaterLevels1.length][initWaterLevels1.length];
		
		int cont1State = 0;
		int cont2State = 0;

		for(int i=0;i<initWaterLevels1.length;i++) {

			for(int j=0;j<initWaterLevels1.length;j++) {
				
                double temptempInitWaterLevel1 = (double) initWaterLevels1[i];
				double temptempInitWaterLevel2 = (double) initWaterLevels1[j];

                int tempInitWaterLevel1 = (int) Math.ceil(temptempInitWaterLevel1/4);
                int tempInitWaterLevel2 = (int) Math.ceil(temptempInitWaterLevel2/4);

                String consts = "wlidInit1=" + (tempInitWaterLevel1) + ",wlidInit2=" + (tempInitWaterLevel2) + ",initContAction1=" + (cont1State) + ",initContAction2=" + (cont2State);
                // String consts = "wlidInit1=13,wlidInit2=13,initContAction1=0,initContAction2=0";

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
		
        String runTimeResults = resultsFolder + "runTimesTwoTankStateTrimming.csv";
        PrintWriter runTimeWriter = new PrintWriter(runTimeResults);
        
        String crashProbResults = resultsFolder + "crashProbsTwoTankStateTrimming.csv";
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

