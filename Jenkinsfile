pipeline {
	agent none

	parameters {
		string (name: 'ENV_NAME', defaultValue: 'Dev19', description: 'Which environment to be used ?')
		string (name : 'HOST_LIST', defaultValue:'hostlist_dev_2', description: 'File name for the hostlist ?')
		string (name : 'HA', defaultValue:'false',description:'HA true/false ?')
		string (name : 'DBCONTAINER', defaultValue:'cdb882',description:'Container DB Name ?')
		string (name : 'DBPLUGGABLE', defaultValue:'pdb882',description:'Pluggable DB Name ?')
	}

	options {
		timestamps()
		
	}
	
	stages {
	
		stage('Tagging the nodes with stop_server tag'){
			agent{
				node{
					label "${CHEF-WORKSTATION}"
				}
			}
			steps{
				script {
					try{
						sh '''
							sudo -S /u01/workstation/chef-repo/knife_tag_assign_role.sh /u01/workstation/chef-repo/${HOST_LIST} stop_servers "recipe[pgbu_reboot_new::stop_servers_V7]"	
						'''
					}
					catch(Exception e){
						sh '''
							echo 'Unable to tag stop_servers'
						'''
						throw e
					}
				}
			}
		}
		
		stage('Stopping servers in App01, App02 , IDM'){
			parallel {
				stage('App01NodeA'){
					agent {
						label "${App01NodeADev19}"
					}
					
					steps {
						sh '''
							cd /tmp
							chef-client -l debug -L stopServer.log
						'''
						script {
							try{
								sh'''
									ps aux | grep /u01/app | awk \'{print $2}\' | xargs kill -9
								'''
							}catch(Exception e){
								throw e
							}
						}
					}
				}
				
				stage('App02NodeA'){
					agent {
						label "${App02NodeADev19}"
					}
					
					steps {
						sh '''
							cd /tmp
							chef-client -l debug -L stopServer.log
						'''
						script{
							try{
								sh'''
									ps aux | grep /u01/app | awk \'{print $2}\' | xargs kill -9
								'''
							}catch(Exception e){
								throw e
							}
						}
					}
				}
				
				stage('IDMNodeA'){
					agent {
						label "${App01NodeADev19}"
					}
					
					steps {
						sh '''
							cd /tmp
							chef-client -l debug -L stopServer.log
						'''
						
						script {
							try{
								sh'''
									ps aux | grep /u01/app | awk \'{print $2}\' | xargs kill -9
								'''
							}catch(Exception e){
								throw e
							}
						}
					}
				}
				
				stage('App01NodeB'){
					agent {
						label "${App01NodeBDev19}"
					}
					steps {
						when (expression { ${HA}==true}){
							sh '''
								cd /tmp
								chef-client -l debug -L stopServer.log
							'''
							script {
								try{
									sh'''
										ps aux | grep /u01/app | awk \'{print $2}\' | xargs kill -9
									'''
								}catch(Exception e){
									throw e
								}
							}
						}
					}
				}
					
				stage('App02NodeB'){
					agent {
						label "${App01NodeBDev19}"
					}
					steps {
						when (expression { ${HA}==true}){
							sh '''
								cd /tmp
								chef-client -l debug -L stopServer.log
							'''
							script{
								try{
									sh'''
										ps aux | grep /u01/app | awk \'{print $2}\' | xargs kill -9
									'''
								}catch(Exception e){
									throw e
								}
							}
						}
					}
				}
					
				stage('IDMNodeB'){
					agent {
						label "${IDMNodeBDev19}"
					}
					steps{
						when (expression { ${HA}==true}){
							sh '''
								cd /tmp
								chef-client -l debug -L stopServer.log
							'''
							script {		
								try{
									sh'''
										ps aux | grep /u01/app | awk \'{print $2}\' | xargs kill -9
									'''
								}catch(Exception e){
									throw e
								}
							}
						}
					}
				}
			}
		}
		
		stage('Stopping database'){ 
			agent {
				label "${DBDev19}"
			}
			steps{
				sh'''
					cd /u01/
					rm -rf stopDB.py   || true
					wget "http://kkm00bme.in.oracle.com:8080/job/Cloud_Automation_BATS/ws/stopDB.py"
					sudo -H -u gbuora python stopDB.py ${DBCONTAINER} ${DBPLUGGABLE} /u01/app/oracle/
				'''
				script {
					try{
						sh'''
							ps aux | grep /u01/app | awk \'{print $2}\' | xargs kill -9
						'''
						}catch(Exception e){
							throw e
						}
				}
			}
		}
		
		stage ('Taking backup'){
			parallel{
				stage('DB Backup'){
					agent {
						label "${DBDev19}"
					}
					steps{
						script{
							try{
								sh'''
									rm -rf /u02/Backup/DB.tar.gz
								'''
								}catch(Exception e){
									throw e
								}
						}
							
						sh'''
							cd /u01
							tar -cvf /u02/Backup/DB.tar.gz app
						'''
					}
				}
				
				stage('App01NodeA Backup'){
					agent {
						label "$App01NodeADev19"
					}
					steps{
						script{	
							try{
								sh'''
									rm -rf /u02/Backup/App01NodeA.tar.gz
								'''
								}catch(Exception e){
									throw e
								}
						}
						sh'''
							cd /u01
							tar -cvf /u02/Backup/App01NodeA.tar.gz app
						'''
					}
				}
				
				stage('App02NodeA Backup'){
					agent {
						label "$App02NodeADev19"
					}
					steps{
						script{
							try{
								sh'''
									rm -rf /u02/Backup/App02NodeA.tar.gz
								'''
								}catch(Exception e){
									throw e
								}
						}
						
						sh'''
							cd /u01
							tar -cvf /u02/Backup/App02NodeA.tar.gz app
						'''
					}
				}
				
				stage('IDMNodeA Backup'){
					agent {
						label "$IDMNodeADev19"
					}
					steps{
						when
						script{
							try{
								sh'''
									rm -rf /u02/Backup/IDMNodeA.tar.gz
								'''
								}catch(Exception e){
									throw e
								}
						}
						
						sh '''
							cd /u01
							tar -cvf /u02/Backup/IDMNodeA.tar.gz app
						'''
					}
				}
				
				stage('App01NodeB Backup'){
					agent {
						label "$App01NodeBDev19"
					}
					steps{
						when (expression { ${HA}==true}){
							script{	
								try{
									sh'''
										rm -rf /u02/Backup/App01NodeB.tar.gz
									'''
									}catch(Exception e){
										throw e
									}
							}
							sh'''
								cd /u01
								tar -cvf /u02/Backup/App01NodeB.tar.gz app
							'''
						}
					}
				}
						
						
				stage('App02NodeB Backup'){
					agent {
						label "$App02NodeBDev19"
					}
					steps{
						when (expression { ${HA}==true}){
							script{
								try{
									sh'''
										rm -rf /u02/Backup/App02NodeB.tar.gz
									'''
									}catch(Exception e){
										throw e
									}
							}	
							sh'''
								cd /u01
								tar -cvf /u02/Backup/App02NodeB.tar.gz app
							'''
						}
					}
				}
				stage('IDMNodeB Backup'){
					agent {
						label "$IDMNodeBDev19"
					}
					steps{
						when (expression { ${HA}==true}){
							script{
								try{
									sh'''
										rm -rf /u02/Backup/IDMNodeB.tar.gz
									'''
									}catch(Exception e){
										throw e
									}
							}	
							sh'''
								cd /u01
								tar -cvf /u02/Backup/IDMNodeB.tar.gz app
							'''
						}
					}
				}
			}
		}
		stage('Starting DB'){
			agent {
				label "${DBDev19}"
			}
			steps{
				sh'''
					cd /u01/
					rm -rf startDB.py   || true
					wget "http://kkm00bme.in.oracle.com:8080/job/Cloud_Automation_BATS/ws/startDB.py"
					sudo -H -u gbuora python startDB.py ${DBCONTAINER} ${DBPLUGGABLE} /u01/app/oracle/
				'''
			}
		}
		
		stage('Tagging the nodes with start_server tag'){
			agent{
				node{
					label "$CHEF-WORKSTATION"
				}
			}
			steps{
				script{
					try{
						sh '''
							sudo -S /u01/workstation/chef-repo/knife_tag_delete_role.sh /u01/workstation/chef-repo/${HOST_LIST} stop_servers
							sudo -S /u01/workstation/chef-repo/knife_tag_assign_role.sh /u01/workstation/chef-repo/${HOST_LIST} start_servers "recipe[pgbu_reboot_new::start_servers_V7]" 
						'''
					}
					catch(Exception e){
						sh '''
							echo 'Unable to tag start_servers'
						'''
					}
				}
			}
		}
		
		stage('Starting servers in App01, App02 , IDM'){
			parallel {
				stage('App01NodeA'){
					agent {
						label "${App01NodeADev19}"
					}
					
					steps {
						sh '''
							cd /tmp
							chef-client -l debug -L stopServer.log
						'''
						
					}
				}
				
				stage('App02NodeA'){
					agent {
						label "${App02NodeADev19}"
					}
					
					steps {
						sh '''
							cd /tmp
							chef-client -l debug -L stopServer.log
						'''
						
					}
				}
				
				stage('IDMNodeA'){
					agent {
						label "${App01NodeADev19}"
					}
					
					steps {
						sh '''
							cd /tmp
							chef-client -l debug -L stopServer.log
						'''
						
					}
				}
				
				stage('App01NodeB'){
					agent {
						label "${App01NodeBDev19}"
					}
					
					steps {
						when (expression { ${HA}==true}){
							sh '''
								cd /tmp
								chef-client -l debug -L stopServer.log
							'''
						}
					}
				}
				
				stage('App02NodeB'){
					agent {
						label "${App02NodeBDev19}"
					}
					steps {
						when (expression { ${HA}==true}){
							sh '''
								cd /tmp
								chef-client -l debug -L stopServer.log
							'''
						}				
					}
				}
				
				stage('IDMNodeB'){
					agent {
						label "${IDMNodeBDev19}"
					}
					
					steps {
						when (expression { ${HA}==true}){
							sh '''
								cd /tmp
								chef-client -l debug -L stopServer.log
							'''
						}
					}
				}
			}
		}
	}
}

