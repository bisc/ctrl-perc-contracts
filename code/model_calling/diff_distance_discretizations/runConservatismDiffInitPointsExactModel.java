package PRISMExperimentsJavaMaven.erhts;

import java.io.PrintWriter;

import prism.PrismException;

public class runConservatismDiffInitPointsExactModel {
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runConservatismDiffInitPointsExactModel () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}

	public static void main (String[] args) throws Exception {
		int initCond2 = 0;        
        String H="3";
        ///// Inflated Baseline
    		double[] distDiscs = {0.04};
    		String[] distDiscsString = {"0.04"};

            
    		String folderName = "C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNewNoRounding\\";
            String fileName = "lecBaselineMajVoteFilterH3L3DistDisc0.04.prism";
            
            String propsFile = "propsForJava.props";
            
            //int[] initDistanceValues = {100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,195,200};
    		//int[] initSpeedValues = {10,14,18,22,26};

    		int[] initDistanceValues = {5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95};
    		int[] initSpeedValues = {10,14,18,22,26};
    		
    		//int[] initDistanceValues = {100,105};
    		//int[] initSpeedValues = {10,14};

    		
            double deltaD = 0.5;

    		double[][] crashProbs = new double[initDistanceValues.length][initSpeedValues.length];
    		double[][] crashProbsDeltad = new double[initDistanceValues.length][initSpeedValues.length];

    		for(int i=0;i<initDistanceValues.length;i++) {
    			for(int j=0;j<initSpeedValues.length;j++) {
    				int initDist = initDistanceValues[i];
    				int initSpeed = initSpeedValues[j];
    				
    				String myModel = folderName + fileName;
    				String myProps = folderName + propsFile;
    				String mypolicy = "";
    				
    				double distDisc = 0.04;
    				double speedDisc = 0.4;
    				
    				int initDist1 = (int) Math.round(initDist/distDisc);
    				int initSpeed1 = (int) Math.round(initSpeed/speedDisc);

                    int initDist2 = (int) Math.round((initDist+deltaD)/distDisc);
    				int initSpeed2 = (int) Math.round(initSpeed/speedDisc);

            		String consts1 = "initPos=" + (initDist1) + ",initSpeed=" + (initSpeed1) + ",initBrakingFlag=0,initBraking=1,carPosThresh=" + (int) Math.round(5/distDisc);
            		String consts2 = "initPos=" + (initDist2) + ",initSpeed=" + (initSpeed2) + ",initBrakingFlag=0,initBraking=1,carPosThresh=" + (int) Math.round(5/distDisc);

    				System.out.println(consts1);
    				PrismConnectorAPI pc= new PrismConnectorAPI();
    				
    				
    		        String res1 = pc.modelCheckFromFileS(myModel,myProps, mypolicy, consts1);
    		        String res2 = pc.modelCheckFromFileS(myModel,myProps, mypolicy, consts2);

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
    		
    		String resultsFolder = "C:\\Users\\matth\\Documents\\Penn\\safetyContract\\experiments_NFM\\conservatismAnalysis\\results\\exp1\\";
    		
            String crashProbsDeltadFile = resultsFolder + "smallDistscrashProbsDeltad.csv";
            PrintWriter crashProbsDeltadWriter = new PrintWriter(crashProbsDeltadFile);
            
            String crashProbResults = resultsFolder + "smallDistscrashProbs.csv";
            PrintWriter crashProbsWriter = new PrintWriter(crashProbResults);
            
            for(int i=0;i<initDistanceValues.length;i++) {
            	for(int j=0; j<initSpeedValues.length;j++) {
            		double tempCrashProbDeltad = crashProbsDeltad[i][j];
            		double tempCrashProb = crashProbs[i][j];
            		if(j==initSpeedValues.length-1) {
            			crashProbsDeltadWriter.print(tempCrashProbDeltad);
            			crashProbsWriter.print(tempCrashProb);
            		}
            		else {
            			crashProbsDeltadWriter.print(tempCrashProbDeltad + ",");
            			crashProbsWriter.print(tempCrashProb + ",");
            		}
            	}
            	crashProbsDeltadWriter.println("");
            	crashProbsWriter.println("");
            }
            
            crashProbsDeltadWriter.close();
            crashProbsWriter.close();
            
	}

		
}
