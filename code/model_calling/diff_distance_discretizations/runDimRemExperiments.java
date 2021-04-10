package PRISMExperimentsJavaMaven.erhts;

import java.io.PrintWriter;

import prism.PrismException;

public class runRamneetExperiments {
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runRamneetExperiments () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		String m = "5";
        String folderNameLattice = "C:\\\\Users\\\\matth\\\\Documents\\\\Penn\\\\safetyContract\\\\ramneetKandNExperiments\\\\pos900.0_v100.0_m" + m + "\\\\";
        //String folderNameLattice = "C:\\\\Users\\\\matth\\\\Documents\\\\Penn\\\\safetyContract\\\\ramneetKandNExperiments\\\\pos1600.0_v200.0_m" + m + "\\\\";
        int[] expNums = {1,2,3,4,5,6,7};
        double[] runTimes = new double[expNums.length];
        double[] crashProbs = new double[expNums.length];
        
        for(int i=0; i<expNums.length;i++) {
        	int trialIter = expNums[i];
        	String myModel = folderNameLattice + "PRISMLECModel" + trialIter + ".prism";
        	String myProps = folderNameLattice + "prop" + trialIter + ".props";
        	
        	
        	System.out.println(myModel);
        	
        	String myPolicy = "";
        	String consts = "";

        	String res = "";
        	int numIter=1;
        	final long startTime = System.nanoTime();

        	for(int j=0;j<numIter;j++) {
        		PrismConnectorAPI pc= new PrismConnectorAPI();
        		res = pc.modelCheckFromFileS(myModel,myProps, myPolicy, consts);
        		pc.close();
        	}
        	final long durationTime = System.nanoTime() - startTime;
        	double ans = Double.parseDouble(res);
        	
        	crashProbs[i] = ans;
        	runTimes[i] = durationTime/numIter;
        	
        	System.out.println(durationTime/1000000000);
        	System.out.println(ans);

        }
        
        String diffDistDiscResultsFileNameLattice = folderNameLattice + "resultsRamneetKandN.csv";
        PrintWriter diffDistDiscResultsWriterLattice = new PrintWriter(diffDistDiscResultsFileNameLattice);
        diffDistDiscResultsWriterLattice.println("DistDisc,crashProb,runtime(ns)");
        for(int i=0;i<expNums.length;i++) {
        	diffDistDiscResultsWriterLattice.println(expNums[i] + "," + crashProbs[i] + "," + runTimes[i]);
        }
        diffDistDiscResultsWriterLattice.close();
        
	}
}
