package PRISMExperimentsJavaMaven.erhts;

import java.io.PrintWriter;

import prism.PrismException;

public class runOlegBaselineExample {
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runOlegBaselineExample () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}

	public static void main (String[] args) throws Exception {
		int initCond2 = 0;        
        String H="3";
        ///// Inflated Baseline
		double[] distDiscs = {0.5,1,2};
		String[] distDiscsString = {"0.500000","1.000000","2.000000"};
		
		//double[] distDiscs = {1};
		//String[] distDiscsString = {"1.000000"};
        
		double[] crashProbs = new double[distDiscs.length];
        double[] runtimes = new double[distDiscs.length];
        
        String folderName = "C:\\Users\\matth\\Documents\\Penn\\safetyContract\\olegBaseline\\constantBraking\\PRISMModels\\testing\\";

        for(int i=0;i<distDiscs.length;i++) {
        	
	        String fileName = "olegBaselineConstLEC" + distDiscsString[i] + ".prism";
	
	    	String propsFile = "olegBaselineProps.props";
	    	
	    	String myModel = folderName + fileName;
	    	String myPolicy = "Unused";
	    	String myProps = folderName + propsFile;
	    	        	
			String consts = "";
	    	
	    	int numIter=1;
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
        String diffDistDiscResultsFileName = folderName + "olegBaselineResultsWithLECBundling.csv";
        PrintWriter diffDistDiscResultsWriter = new PrintWriter(diffDistDiscResultsFileName);
        diffDistDiscResultsWriter.println("DistDisc,crashProb,runtime(ns)");
        for(int i=0;i<distDiscsString.length;i++) {
        	diffDistDiscResultsWriter.println(distDiscsString[i] + "," + crashProbs[i] + "," + runtimes[i]);
        }
        diffDistDiscResultsWriter.close();
            // */
            
            
	}

		
}
