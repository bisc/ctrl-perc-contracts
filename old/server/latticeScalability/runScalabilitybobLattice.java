import java.io.PrintWriter;

import prism.PrismException;
//import PRISMConnectorAPI

public class runScalabilitybobLattice {

	
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runScalabilitybobLattice () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		String N = "3";
		String H = "3";
		String L = "3";
		String d = "15";
		
		String latticeFolder = "/data2/mcleav/latticeScalability/latticeModels/N" + N + "H" + H + "L" + L + "d" + d + "/bobLattice/";
		String propsFile = "/data2/mcleav/latticeScalability/props3.props";
		
		//int[] initDistanceValues = {120,130,140,150,160,170,180};
		//int[] initSpeedValues = {10,14,18,22,26,30};
		
		int[] initDistanceValues = {145,150,155,160,165,170,175,180,185,190,195,200};
		int[] initSpeedValues = {10,14,18,22,26};

		//int[] initDistanceValues = {120,125};
		//int[] initSpeedValues = {10,12};
		double[][] runTimes = new double[initDistanceValues.length][initSpeedValues.length];
		double[][] crashProbs = new double[initDistanceValues.length][initSpeedValues.length];
		
		for(int i=0;i<initDistanceValues.length;i++) {
			for(int j=0;j<initSpeedValues.length;j++) {
				int initDist = initDistanceValues[i];
				int initSpeed = initSpeedValues[j];
				
				String myModelName = "BoBLatticeScalabilityN" + N + "H" + H + "L" + L + "d" + d + "_initd" + initDist + ".000000_initv" + initSpeed + ".000000.prism";
				String myModel = latticeFolder + myModelName;
				
				String mypolicy = "";
				String consts = "";
				
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
		
        String runTimeResults = resultsFolder + "extraextraPointsrunTimesBoBLatticeN" + N + "H" + H + "L" + L + "d" + d + ".csv";
        PrintWriter runTimeWriter = new PrintWriter(runTimeResults);
        
        String crashProbResults = resultsFolder + "extraextraPointscrashProbsBoBLatticeN" + N + "H" + H + "L" + L + "d" + d + ".csv";
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
