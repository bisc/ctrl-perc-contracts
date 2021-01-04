package PRISMExperimentsJavaMaven.erhts;

import java.io.PrintWriter;

import prism.PrismException;

public class runNoRoundingBaseline {
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runNoRoundingBaseline () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}

	public static void main (String[] args) throws Exception {
		int initCond2 = 0;        
        String H="3";
        ///// Inflated Baseline
    		double[] distDiscs = {0.04};
    		String[] distDiscsString = {"0.04"};
            double[] crashProbs = new double[distDiscs.length];
            double[] runtimes = new double[distDiscs.length];
            
    		String folderName = "C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNewNoRounding\\";
            String fileNameBase = "lecBaselineMajVoteFilterH" + H + "L3DistDisc";
            String fileNameBaseEnd = ".prism";
            for(int i=0;i<distDiscs.length;i++) {
            	double distDisc = distDiscs[i];
            	String propsFile = "propsForJava.props";
            	
            	String myModel = folderName + fileNameBase + distDiscsString[i] + fileNameBaseEnd;
            	String myPolicy = "Unused";
            	String myProps = folderName + propsFile;
            	        	
        		int initDist = (int) Math.round(166/distDisc);
        		int initSpeed = 50;
        		
        		if(initCond2==1) {
        			initDist = (int) Math.round(90/distDisc);
        			initSpeed = 25;
        		}
        		
        		String consts = "initPos=" + (initDist) + ",initSpeed=" + (initSpeed)+ ",initBrakingFlag=0,initBraking=1,carPosThresh=" + (int) Math.round(5/distDisc);
            	
            	int numIter=3;
            	String res1 = "";
            	final long startTime = System.nanoTime();

            	for(int j=0;j<numIter;j++) {
            		PrismConnectorAPI pc= new PrismConnectorAPI();
            		res1 = pc.modelCheckFromFileS(myModel,myProps, myPolicy, consts);
            		pc.close();
            	}
            	final long durationTime = System.nanoTime() - startTime;
            	double ans = Double.parseDouble(res1);
    		
            	System.out.println(durationTime/(1000000000*numIter));
            	System.out.println(ans);
            	
                crashProbs[i]=ans;
                runtimes[i]=durationTime/numIter;

            }
            
            
            String diffDistDiscResultsFileName = folderName + "diffDistDiscresultsMajVoteFilterH" + H + "L3Temp.csv";
            if(initCond2==1) {
            	diffDistDiscResultsFileName = folderName + "diffDistDiscresultsMajVoteFilterH" + H + "L3TempInitCond2.csv";
            }
            PrintWriter diffDistDiscResultsWriter = new PrintWriter(diffDistDiscResultsFileName);
            diffDistDiscResultsWriter.println("DistDisc,crashProb,runtime(ns)");
            for(int i=0;i<distDiscsString.length;i++) {
            	diffDistDiscResultsWriter.println(distDiscsString[i] + "," + crashProbs[i] + "," + runtimes[i]);
            }
            diffDistDiscResultsWriter.close();
            // */
            
            
	}

		
}
