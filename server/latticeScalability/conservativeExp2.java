import java.io.PrintWriter;

import prism.PrismException;
//import PRISMConnectorAPI

public class conservativeExp2 {

	
	PrismConnectorAPI myPrismConnectorAPI;
	
	public conservativeExp2 () throws PrismException {
		myPrismConnectorAPI = new PrismConnectorAPI();
	}
	
	public static void main (String[] args) throws Exception {
		
		String baselineFolder = "/data2/mcleav/latticeScalability/baselineModels/exactBaseline/";
		String propsFile = "/data2/mcleav/latticeScalability/propsForJava.props";

        //int initDistLower = 160;
        //int initDistUpper = 210;

        //int initDistLower = 100;
        //double initDistUpper = 155.5;

        //int initDistLower = 156;
        //double initDistUpper = 159.5;

        double initDistLower = 0.5;
        double initDistUpper = 99.5;

        double distanceDisc = 0.5;

        int initSpeed = 20;

        int numPoints = (int) Math.round((initDistUpper-initDistLower)/distanceDisc+1);
		double[] crashProbs = new double[numPoints];

        int iter = 0;
		for(double i=initDistLower;i<=initDistUpper;i+=distanceDisc) {
            double initDist = i;
            System.out.println(initDist);
            
            String myModelName = "lecBaselineMajVoteFilterH3L3DistDisc0.04.prism";
            String myModel = baselineFolder + myModelName;
            
            double distDisc = 0.04;
            double speedDisc = 0.4;
            String mypolicy = "";

            int initDist1 = (int) Math.round(initDist/distDisc);
            int initSpeed1 = (int) Math.round(initSpeed/speedDisc);

            String consts1 = "initPos=" + (initDist1) + ",initSpeed=" + (initSpeed1) + ",initBrakingFlag=0,initBraking=1,carPosThresh=" + (int) Math.round(5/distDisc);

            System.out.println(consts1);
            PrismConnectorAPI pc= new PrismConnectorAPI();
            String res1 = pc.modelCheckFromFileS(myModel,propsFile, mypolicy, consts1);
            pc.close();

            double ans1 = Double.parseDouble(res1);
            crashProbs[iter] = ans1;
            iter++;

		}
		
		String resultsFolder = "/data2/mcleav/latticeScalability/results/conservatism/exp2/";
		
        
        String crashProbResults = resultsFolder + "smallInitDistsextraPointscrashProbsExactBaseline.csv";
        PrintWriter crashProbsWriter = new PrintWriter(crashProbResults);
        for(int i=0;i<crashProbs.length;i++) {
            double tempCrashProb = crashProbs[i];
            crashProbsWriter.print(tempCrashProb);
            if(i!=crashProbs.length-1){
                crashProbsWriter.print(',');
            }
        }
        
        crashProbsWriter.close();
	}
		
}
