package PRISMExperimentsJavaMaven.erhts;

import java.io.PrintWriter;

import prism.PrismException;

public class runAEBSLatticeWindowDiffDistDiscs {
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runAEBSLatticeWindowDiffDistDiscs () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		int initDist = 1660;
		//int initDist = 75;
		int initSpeed = 200;
		
        String res="result";
        
        String folderName = "C:\\\\Users\\\\matth\\\\Documents\\\\Penn\\\\safetyContract\\\\lattice\\\\matlabCode\\\\simpleExample\\\\PRISMModels\\\\ForPaper\\\\windows\\\\N3H3L3\\\\diffDeltaDsBoBLattice\\\\";
        
        double[] distDiscs = {0.5, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.65, 1.7, 1.75, 1.8, 1.9, 2};
        double[] crashProbs = new double[distDiscs.length];
        double[] runtimes = new double[distDiscs.length];
        
        
        String fileNameBase = "latticePRISMModelTrimmedCondLECN3H3L3d";
        String fileNameBaseEnd = ".prism";
        String[] fileNames = {"0.500000","1.000000","1.100000","1.200000","1.300000","1.400000","1.500000","1.600000","1.650000","1.700000","1.750000","1.800000","1.900000","2.000000"};
        for(int i=0;i<fileNames.length;i++) {
        	System.out.println(fileNameBase + fileNames[i] + fileNameBaseEnd);
        	double distDisc = distDiscs[i];

        	String propsFile = "";
        	if(distDisc>=1.5) {
        		propsFile = "props3.props";
        	}
        	else if(distDisc>=1.25) {
        		propsFile = "props4.props";
        	}
        	else if(distDisc>=1) {
        		propsFile = "props5.props";
        	}
        	else if(distDisc>=0.75) {
        		propsFile = "props7.props";
        	}
        	else if(distDisc>=0.5) {
        		propsFile = "props10.props";
        	}
        	else {
        		propsFile = "props20.props";
        	}
        	
        	String myModel = folderName + fileNameBase + fileNames[i] + fileNameBaseEnd;
        	String myPolicy = "Unused";
        	String myProps = folderName + propsFile;
        	
        	String consts = "";
        	
        	int numIter=3;
        	final long startTime = System.nanoTime();

        	for(int j=0;j<numIter;j++) {
        		PrismConnectorAPI pc= new PrismConnectorAPI();
        		res = pc.modelCheckFromFileS(myModel,myProps, myPolicy, consts);
        		pc.close();
        	}
        	final long durationTime = System.nanoTime() - startTime;
        	double ans = Double.parseDouble(res);
            
            System.out.println("Done Running PRISM");
            System.out.println(durationTime/(numIter*1000000000));
            System.out.println(ans);
            
            crashProbs[i]=ans;
            runtimes[i]=durationTime/numIter;

        }
        
        String diffDistDiscResultsFileName = folderName + "results.csv";
        PrintWriter diffDistDiscResultsWriter = new PrintWriter(diffDistDiscResultsFileName);
        diffDistDiscResultsWriter.println("DistDisc,crashProb,runtime(ns)");
        for(int i=0;i<fileNames.length;i++) {
        	diffDistDiscResultsWriter.println(distDiscs[i] + "," + crashProbs[i] + "," + runtimes[i]);
        }
        diffDistDiscResultsWriter.close();
	}

}
