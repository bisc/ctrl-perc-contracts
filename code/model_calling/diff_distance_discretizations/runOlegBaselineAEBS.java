package PRISMExperimentsJavaMaven.erhts;

import java.io.PrintWriter;

import prism.PrismException;

public class runOlegBaselineAEBS {
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runOlegBaselineAEBS () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}

	public static void main (String[] args) throws Exception {
		int initCond2 = 0;        
        String H="3";
        int rounding = 0;

        ///// Inflated Baseline
		double[] distDiscs = {0.2,0.25,0.4,0.5,1,2};
		String[] distDiscsString = {"0.200000","0.250000","0.400000","0.500000","1.000000","2.000000"};
		
		//double[] distDiscs = {1};
		//String[] distDiscsString = {"1.000000"};
        
		double[] crashProbs = new double[distDiscs.length];
        double[] runtimes = new double[distDiscs.length];
        
        String folderName = "C:\\Users\\matth\\Documents\\Penn\\safetyContract\\olegBaseline\\AEBS\\PRISMModels\\testingFixedRounding\\";
        String roundingString="";
        if(rounding==1) {
        	roundingString="WithRounding";
        } else {
        	roundingString="NoRounding";
        }
        
        String initCondString = "";
        if(initCond2==1) {
        	initCondString = "InitCond2";
        } else {
        	initCondString = "InitCond1";
        }
        	
        for(int i=0;i<distDiscs.length;i++) {
        	
	        String fileName = "olegBaselineAEBSConstLEC" + initCondString + roundingString + distDiscsString[i] + ".prism";
	
	    	String propsFile = "olegBaselineProps.props";
	    	
	    	String myModel = folderName + fileName;
	    	String myPolicy = "Unused";
	    	String myProps = folderName + propsFile;
	    	        	
			String consts = "";
	    	
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
	    	
	    	runtimes[i]=durationTime/numIter;
	    	crashProbs[i]=ans;
        }
        String diffDistDiscResultsFileName = folderName + "olegBaselineAEBS" + roundingString + "Results" + initCondString + ".csv";
        PrintWriter diffDistDiscResultsWriter = new PrintWriter(diffDistDiscResultsFileName);
        diffDistDiscResultsWriter.println("DistDisc,crashProb,runtime(ns)");
        for(int i=0;i<distDiscsString.length;i++) {
        	diffDistDiscResultsWriter.println(distDiscsString[i] + "," + crashProbs[i] + "," + runtimes[i]);
        }
        diffDistDiscResultsWriter.close();
            // */
            
            
	}

		
}
