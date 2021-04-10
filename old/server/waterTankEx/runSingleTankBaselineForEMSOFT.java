import java.io.PrintWriter;

import prism.PrismException;
//import PRISMConnectorAPI

public class runSingleTankBaselineForEMSOFT {

	
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runSingleTankBaselineForEMSOFT () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		
		String waterTankFolder = "/data2/mcleav/waterTankEx/singleTankEx/";
        String propsFile = "/data2/mcleav/waterTankEx/doubleTankExStateTrimming/intBaselineProps.props";
        String myModelName = "singleTankEMSOFT.prism";
        String myModel = waterTankFolder + myModelName;
        String mypolicy = "";

		double[] runTimes = new double[101];
		double[] crashProbs = new double[101];
		
		int cont1State = 0;
		int cont2State = 0;

		for(int i=0;i<101;i++) {
            int tempInitWaterLevel1 = i;

            String consts = "wlidInit1=" + (tempInitWaterLevel1) + ",initContAction1=" + (cont1State);

            System.out.println(consts);
            PrismConnectorAPI pc= new PrismConnectorAPI();
            
            
            final long startTime = System.nanoTime();
            String res = pc.modelCheckFromFileS(myModel,propsFile, mypolicy, consts);
            long durationTime = (System.nanoTime() - startTime);
            pc.close();
            double ans = Double.parseDouble(res);

            runTimes[i] = durationTime;
            crashProbs[i] = ans;


            System.out.println(myModelName);
            System.out.println(ans);
            System.out.println((double) (durationTime)/(1000000000));
                


        }

		String resultsFolder = "/data2/mcleav/waterTankEx/EMSOFTResults/singleTank/";
		
        String runTimeResults = resultsFolder + "runTimesSingleTankBaseline.csv";
        PrintWriter runTimeWriter = new PrintWriter(runTimeResults);
        
        String crashProbResults = resultsFolder + "crashProbsSingleTankBaseline.csv";
        PrintWriter crashProbsWriter = new PrintWriter(crashProbResults);
        for(int i=0;i<101;i++) {
            double tempRunTime = runTimes[i];
            double tempCrashProb = crashProbs[i];
            if(i==100) {
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

