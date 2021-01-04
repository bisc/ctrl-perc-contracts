package PRISMExperimentsJavaMaven.erhts;

import java.io.PrintWriter;

import prism.PrismException;

public class runBaselineModelDiffDistDiscs {
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runBaselineModelDiffDistDiscs () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		
		///// Baseline
		//double[] distDiscs = {0.1,0.5,1,1.5,2};
		//String[] distDiscsString = {"0.1","0.5","1","1.5","2"};
		
		double[] distDiscs = {0.25,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1};
		String[] distDiscsString = {"0.25","0.3","0.4","0.5","0.6","0.7","0.8","0.9","1"};
        double[] crashProbs = new double[distDiscs.length];
        double[] runtimes = new double[distDiscs.length];
        
		String folderName = "C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\baselineModelExperiments\\windowed\\diffDistDiscsNew\\";
        String fileNameBase = "lecBaselineMajVoteFilterH3L3DistDisc";
        String fileNameBaseEnd = ".prism";
        for(int i=0;i<distDiscs.length;i++) {
        	double distDisc = distDiscs[i];
        	String propsFile = "propsForJava.props";
        	
        	String myModel = folderName + fileNameBase + distDiscsString[i] + fileNameBaseEnd;
        	String myPolicy = "Unused";
        	String myProps = folderName + propsFile;
        	
        	double speedDisc = 0.4;
        	        	
    		int initDist = (int) Math.round(166/distDisc);
    		int initSpeed = (int) Math.round(20/speedDisc);
    		System.out.println((int) Math.round(0/distDisc));
    		String consts = "initPos=" + (initDist) + ",initSpeed=" + (initSpeed)+ ",initBrakingFlag=0,initBraking=1,carPosThresh=" + (int) Math.round(5/distDisc);
        	
        	int numIter=1;
        	String res = "";
        	final long startTime = System.nanoTime();

        	for(int j=0;j<numIter;j++) {
        		PrismConnectorAPI pc= new PrismConnectorAPI();
        		res = pc.modelCheckFromFileS(myModel,myProps, myPolicy, consts);
        		pc.close();
        	}
        	final long durationTime = System.nanoTime() - startTime;
        	double ans = Double.parseDouble(res);
		
        	System.out.println(durationTime/(1000000000*numIter));
        	System.out.println(ans);
        	
            crashProbs[i]=ans;
            runtimes[i]=durationTime/numIter;

        }
        
        
        String diffDistDiscResultsFileName = folderName + "diffDistDiscresultsMajVoteFilterH3L3Temp.csv";
        PrintWriter diffDistDiscResultsWriter = new PrintWriter(diffDistDiscResultsFileName);
        diffDistDiscResultsWriter.println("DistDisc,crashProb,runtime(ns)");
        for(int i=0;i<distDiscsString.length;i++) {
        	diffDistDiscResultsWriter.println(distDiscsString[i] + "," + crashProbs[i] + "," + runtimes[i]);
        }
        diffDistDiscResultsWriter.close();
        // */
        
        ///// Lattice
        /*String res="result";
        
        String folderNameLattice = "C:\\\\Users\\\\matth\\\\Documents\\\\Penn\\\\safetyContract\\\\lattice\\\\matlabCode\\\\simpleExample\\\\PRISMModels\\\\ForPaper\\\\windows\\\\N3H3L3\\\\diffDeltaDs\\\\";
        
        //double[] distDiscsLattice = {1.25,1.5,1.55,1.75};
        double[] distDiscsLattice = {1.55};
        double[] crashProbsLattice = new double[distDiscsLattice.length];
        double[] runtimesLattice = new double[distDiscsLattice.length];
        
        String fileNameBaseLattice = "latticePRISMModelTrimmedCondLECN3H3L3d";
        String fileNameBaseEndLattice = ".prism";
        //String[] fileNamesLattice = {"1.000000","1.250000","1.500000","1.55","1.750000"};
        String[] fileNamesLattice = {"1.550000"};
        for(int i=0;i<fileNamesLattice.length;i++) {
        	System.out.println(fileNameBaseLattice + fileNamesLattice[i] + fileNameBaseEndLattice);
        	double distDiscLattice = distDiscsLattice[i];

        	String propsFileLattice = "";
        	if(distDiscLattice>=1.5) {
        		propsFileLattice = "props3.props";
        	}
        	else if(distDiscLattice>=1.25) {
        		propsFileLattice = "props4.props";
        	}
        	else if(distDiscLattice>=1) {
        		propsFileLattice = "props5.props";
        	}
        	else if(distDiscLattice>=0.75) {
        		propsFileLattice = "props7.props";
        	}
        	else if(distDiscLattice>=0.5) {
        		propsFileLattice = "props10.props";
        	}
        	else {
        		propsFileLattice = "props20.props";
        	}
        	
        	String myModel = folderNameLattice + fileNameBaseLattice + fileNamesLattice[i] + fileNameBaseEndLattice;
        	String myPolicy = "Unused";
        	String myProps = folderNameLattice + propsFileLattice;
        	
        	String consts = "";
        	
        	int numIter=1;
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
            
            crashProbsLattice[i]=ans;
            runtimesLattice[i]=durationTime/numIter;

        }
        
        /*String diffDistDiscResultsFileNameLattice = folderNameLattice + "resultsTemp.csv";
        PrintWriter diffDistDiscResultsWriterLattice = new PrintWriter(diffDistDiscResultsFileNameLattice);
        diffDistDiscResultsWriterLattice.println("DistDisc,crashProb,runtime(ns)");
        for(int i=0;i<fileNamesLattice.length;i++) {
        	diffDistDiscResultsWriterLattice.println(distDiscsLattice[i] + "," + crashProbsLattice[i] + "," + runtimesLattice[i]);
        }
        diffDistDiscResultsWriterLattice.close();
		// */
	}

}
