clear all
load population;
 sampleSize = size(unique(population(:,1)),1);
 NumTurns = 20;
 NumTrials = 30;
 TotalTrials = sampleSize*NumTrials;
 
 
 ExEx =[]; 
 Switch = [];
 RT= [];
 
 for i = 1 : TotalTrials
     WholeExEx = population((20*(i-1)+2):(20*(i-1)+20),4);
     WholeSwitch = population((20*(i-1)+2):(20*(i-1)+20),5);
     WholeRT = population((20*(i-1)+2):(20*(i-1)+20),7);
     
     ExEx = [ExEx;WholeExEx];
     Switch = [Switch; WholeSwitch];
     RT= [RT;WholeRT];
 end
 
 firstExEx =[]; 
 firstSwitch = [];
 firstRT= [];
 middleExEx =[]; 
 middleSwitch = [];
 middleRT= [];
 lastExEx =[]; 
 lastSwitch = [];
 lastRT= [];
 for i = 1 : sampleSize
     ExExfirst = ExEx((570*(i-1)+1):(570*(i-1)+190),1);
     ExExmiddle =ExEx((570*(i-1)+191):(570*(i-1)+380),1); 
     ExExlast = ExEx((570*(i-1)+381):(570*(i-1)+570),1);
     
     Switchfirst = Switch((570*(i-1)+1):(570*(i-1)+190),1);
     Switchmiddle =Switch((570*(i-1)+191):(570*(i-1)+380),1); 
     Switchlast = Switch((570*(i-1)+381):(570*(i-1)+570),1);
     
     RTfirst = RT((570*(i-1)+1):(570*(i-1)+190),1);
     RTmiddle =RT((570*(i-1)+191):(570*(i-1)+380),1); 
     RTlast = RT((570*(i-1)+381):(570*(i-1)+570),1);
     
 firstExEx =[firstExEx; ExExfirst]; 
 middleExEx =[middleExEx;ExExmiddle];
 lastExEx =[lastExEx;ExExlast]; 
 firstSwitch = [firstSwitch; Switchfirst];
 middleSwitch = [middleSwitch; Switchmiddle];
 lastSwitch = [lastSwitch;Switchlast ];
 firstRT= [firstRT; RTfirst];
 middleRT= [middleRT;RTmiddle];
 lastRT= [lastRT;RTlast];
 
 end

  
  
  
  
  
 firstExploreTime =[];
 firstExploitTime=[];
 firstSwitchTime=[];
 firstNonSwitchTime=[];
 firstSwitchToExploreTime = [];
 firstSwitchToExploitTime = [];
 
 
 middleExploreTime =[];
 middleExploitTime=[];
 middleSwitchTime=[];
 middleNonSwitchTime=[];
 middleSwitchToExploreTime = [];
 middleSwitchToExploitTime = [];
 
 lastExploreTime =[];
 lastExploitTime=[];
 lastSwitchTime=[];
 lastNonSwitchTime=[];
 lastSwitchToExploreTime = [];
 lastSwitchToExploitTime = [];
 
 for i = 1 : sampleSize
      firstEachExEx = firstExEx((190*(i-1)+1):(190*(i-1)+190),1);
      firstEachSwitch = firstSwitch((190*(i-1)+1):(190*(i-1)+190),1);
      firstEachRT = firstRT((190*(i-1)+1):(190*(i-1)+190),1);
      
      
      firstEachExploreTime = sum(firstEachRT(firstEachExEx == 0))/size(firstEachRT(firstEachExEx == 0),1);
      firstEachExploitTime = sum(firstEachRT(firstEachExEx == 1))/size(firstEachRT(firstEachExEx == 1),1);
      firstEachSwitchTime =  sum(firstEachRT(firstEachSwitch == 1))/size(firstEachRT(firstEachSwitch == 1),1);
      firstEachNonSwitchTime = sum(firstEachRT(firstEachSwitch == 0))/size(firstEachRT(firstEachSwitch == 0),1);
      %%%%%%%%%%%%(EachSwitch == 1)&(EachExEx == 0): note this would return
      %%%%%%%%%%%%a same size of a matrix with logic value 0 or 1. and then
      %%%%%%%%%%%%matlab match it with the outside matrix's elements
      firstEachSwitchToExploreTime = sum(firstEachRT((firstEachSwitch == 1)&(firstEachExEx == 0)))/...
          size(firstEachRT((firstEachSwitch == 1)&(firstEachExEx == 0)),1);
      firstEachSwitchToExploitTime = sum(firstEachRT((firstEachSwitch == 1)&(firstEachExEx == 1)))/...
          size(firstEachRT((firstEachSwitch == 1)&(firstEachExEx == 1)),1);
      
 firstExploreTime =[firstExploreTime ; firstEachExploreTime];
 firstExploitTime=[firstExploitTime; firstEachExploitTime];
 firstSwitchTime=[firstSwitchTime;firstEachSwitchTime ];
 firstNonSwitchTime=[firstNonSwitchTime; firstEachNonSwitchTime];
 firstSwitchToExploreTime = [firstSwitchToExploreTime; firstEachSwitchToExploreTime];
 %%Nan means never swtich to explore again!!
 firstSwitchToExploitTime = [firstSwitchToExploitTime; firstEachSwitchToExploitTime];
 
 
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%middle
  middleEachExEx = middleExEx((190*(i-1)+1):(190*(i-1)+190),1);
      middleEachSwitch = middleSwitch((190*(i-1)+1):(190*(i-1)+190),1);
      middleEachRT = middleRT((190*(i-1)+1):(190*(i-1)+190),1);
      
      
      middleEachExploreTime = sum(middleEachRT(middleEachExEx == 0))/size(middleEachRT(middleEachExEx == 0),1);
      middleEachExploitTime = sum(middleEachRT(middleEachExEx == 1))/size(middleEachRT(middleEachExEx == 1),1);
      middleEachSwitchTime =  sum(middleEachRT(middleEachSwitch == 1))/size(middleEachRT(middleEachSwitch == 1),1);
      middleEachNonSwitchTime = sum(middleEachRT(middleEachSwitch == 0))/size(middleEachRT(middleEachSwitch == 0),1);
      %%%%%%%%%%%%(EachSwitch == 1)&(EachExEx == 0): note this would return
      %%%%%%%%%%%%a same size of a matrix with logic value 0 or 1. and then
      %%%%%%%%%%%%matlab match it with the outside matrix's elements
      middleEachSwitchToExploreTime = sum(middleEachRT((middleEachSwitch == 1)&(middleEachExEx == 0)))/...
          size(middleEachRT((middleEachSwitch == 1)&(middleEachExEx == 0)),1);
      middleEachSwitchToExploitTime = sum(middleEachRT((middleEachSwitch == 1)&(middleEachExEx == 1)))/...
          size(middleEachRT((middleEachSwitch == 1)&(middleEachExEx == 1)),1);
      
 middleExploreTime =[middleExploreTime ; middleEachExploreTime];
 middleExploitTime=[middleExploitTime; middleEachExploitTime];
 middleSwitchTime=[middleSwitchTime;middleEachSwitchTime ];
 middleNonSwitchTime=[middleNonSwitchTime; middleEachNonSwitchTime];
 middleSwitchToExploreTime = [middleSwitchToExploreTime; middleEachSwitchToExploreTime];
 %%Nan means never swtich to explore again!!
 middleSwitchToExploitTime = [middleSwitchToExploitTime; middleEachSwitchToExploitTime];
 
 
 %%%%%%%%%%%%%%%%%last 10 trials%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
 lastEachExEx = lastExEx((190*(i-1)+1):(190*(i-1)+190),1);
      lastEachSwitch = lastSwitch((190*(i-1)+1):(190*(i-1)+190),1);
      lastEachRT = lastRT((190*(i-1)+1):(190*(i-1)+190),1);
      
      
      lastEachExploreTime = sum(lastEachRT(lastEachExEx == 0))/size(lastEachRT(lastEachExEx == 0),1);
      lastEachExploitTime = sum(lastEachRT(lastEachExEx == 1))/size(lastEachRT(lastEachExEx == 1),1);
      lastEachSwitchTime =  sum(lastEachRT(lastEachSwitch == 1))/size(lastEachRT(lastEachSwitch == 1),1);
      lastEachNonSwitchTime = sum(lastEachRT(lastEachSwitch == 0))/size(lastEachRT(lastEachSwitch == 0),1);
      %%%%%%%%%%%%(EachSwitch == 1)&(EachExEx == 0): note this would return
      %%%%%%%%%%%%a same size of a matrix with logic value 0 or 1. and then
      %%%%%%%%%%%%matlab match it with the outside matrix's elements
      lastEachSwitchToExploreTime = sum(lastEachRT((lastEachSwitch == 1)&(lastEachExEx == 0)))/...
          size(lastEachRT((lastEachSwitch == 1)&(lastEachExEx == 0)),1);
      lastEachSwitchToExploitTime = sum(lastEachRT((lastEachSwitch == 1)&(lastEachExEx == 1)))/...
          size(lastEachRT((lastEachSwitch == 1)&(lastEachExEx == 1)),1);
      
 lastExploreTime =[lastExploreTime ; lastEachExploreTime];
 lastExploitTime=[lastExploitTime; lastEachExploitTime];
 lastSwitchTime=[lastSwitchTime;lastEachSwitchTime ];
 lastNonSwitchTime=[lastNonSwitchTime; lastEachNonSwitchTime];
 lastSwitchToExploreTime = [lastSwitchToExploreTime; lastEachSwitchToExploreTime];
 %%Nan means never swtich to explore again!!
 lastSwitchToExploitTime = [lastSwitchToExploitTime; lastEachSwitchToExploitTime];
 
 end
      %%%%%%%%%%%%%%%%%%%%%%
      mean(firstExploreTime)
       mean(middleExploreTime)
        mean(lastExploreTime)
        
        
        %%%%%%%%%%%%%%%%%%%%%%%
       NaNfirstExploitTime = firstExploitTime(~isnan(firstExploitTime));
       mean(NaNfirstExploitTime)
       mean(middleExploitTime)
       mean(lastExploitTime)
       
       %%%%%%%%%%%%%%%%%%%%
      NaNfirstSwitchTime = firstSwitchTime(~isnan(firstSwitchTime));
      mean(NaNfirstSwitchTime)
      mean(middleSwitchTime)
      mean(lastSwitchTime)
      
      
      %%%%%%%%%%%%%%%%%%%5
      mean(firstNonSwitchTime)
      mean(middleNonSwitchTime)
      mean(lastNonSwitchTime)
      
      %%%%%%%%%
      NaNfirstSwitchToExploreTime = firstSwitchToExploreTime...
          (~isnan(firstSwitchToExploreTime));
      mean(NaNfirstSwitchToExploreTime)
      NaNmiddleSwitchToExploreTime = middleSwitchToExploreTime...
          (~isnan(middleSwitchToExploreTime));
      mean(NaNmiddleSwitchToExploreTime)
      NaNlastSwitchToExploreTime = lastSwitchToExploreTime...
          (~isnan(lastSwitchToExploreTime));
      mean(NaNlastSwitchToExploreTime)
      
      %%%%%%%%%%%%%%%%%%%%%%%%%%
      NaNfirstSwitchToExploitTime = firstSwitchToExploitTime...
          (~isnan(firstSwitchToExploitTime));
      mean(NaNfirstSwitchToExploitTime)
      mean(middleSwitchToExploitTime)
      mean(lastSwitchToExploitTime)
     
    
      
      
      
      
      
     
     
      
      
      
      
      