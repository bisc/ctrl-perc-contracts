package PRISMExperimentsJavaMaven.erhts;

import java.io.PrintWriter;

import prism.PrismException;

public class runRamneetKAndN {
	PrismConnectorAPI myPrismConnectorAPI;
	
	public runRamneetKAndN () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		int initDist = 1660;
		//int initDist = 75;
		int initSpeed = 200;
		
        String res="result";
        
        // Lattice with cond lec
        String latticeModelTrimmedCondLEC = "C:\\Users\\matth\\Documents\\Penn\\safetyContract\\PRISM\\ramneetKAndN\\\\PRISMLECModelNewNew.prism";
        String latticePolicyTrimmedCondLEC = "Unused";
        String latticePropsTrimmedCondLEC = "C:\\\\Users\\\\matth\\\\Documents\\\\Penn\\\\safetyContract\\\\PRISM\\\\ramneetKAndN\\\\AEBSIntervalKoutofNNewNew.props";

        String consts = "initPos=" + (initDist) + ",initSpeed=" + (initSpeed)+ ",initBrakingFlag=0,initBraking=1";
        PrismConnectorAPI pc= new PrismConnectorAPI();

        //PrismConnectorAPI pc= new PrismConnectorAPI();
        final long startTimeLatticeTrimmedCondLEC = System.nanoTime();
        consts = "";
        String resLatticeTrimmedCondLEC = "result";
        resLatticeTrimmedCondLEC = pc.modelCheckFromFileS(latticeModelTrimmedCondLEC,latticePropsTrimmedCondLEC, latticePolicyTrimmedCondLEC, consts);
        final long durationLatticeTrimmedCondLEC = System.nanoTime() - startTimeLatticeTrimmedCondLEC;
        pc.close();
        double ansLatticeTrimmedCondLEC = Double.parseDouble(resLatticeTrimmedCondLEC);
        
        
        
        System.out.println("Done Running PRISM");
        
        System.out.println(durationLatticeTrimmedCondLEC/1000000000);
        System.out.println(ansLatticeTrimmedCondLEC);

	}

}
