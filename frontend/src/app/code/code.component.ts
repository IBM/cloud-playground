import { Component, OnInit , Renderer2 } from '@angular/core';
import { FileuploadService } from '../fileupload.service';
import { faFrown } from '@fortawesome/free-solid-svg-icons';
import { timer, Observable, Subject, of } from 'rxjs';
import { switchMap, takeUntil, catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-code',
  templateUrl: './code.component.html',
  styleUrls: ['./code.component.css']
})

export class CodeComponent implements OnInit {

  public data:string='';
  public lastClicked="Python";
  public extensionMap = new Map([
    ["Python",".py"],
    ["Java",".java"],
    ["Go",".go"],
    ["Node",".js"]
  ])
  public allowedLanguages=["Go","Java","Node","Python"];
  public lightTheme:boolean=false;
  public loadingOutput:boolean=false;
  public runButtonDisable:boolean=false;
  public errorOccured:boolean=false
  public faFrown=faFrown;
  public displayOutput:boolean=false
  public output:string='';
  public uniquekey:any={}
  public waitMsg:string="Waiting for remote server..."
  private killTrigger: Subject<void> = new Subject();
  private fetchData$=this.uploadSevice.getResults(this.uniquekey);
  private refreshInterval$: Observable<number> = timer(0, 20000)


  statusText: any;

// correct tha value of text are
// correct the run code function
  constructor(private uploadSevice: FileuploadService , private render : Renderer2) { }

  ngOnInit(){
    this.uploadSevice.readFile('Python').subscribe((c:string)=>{
      this.data=c;
      this.render.setStyle(this.render.selectRootElement("#Python",true),"border-bottom","2px solid #0f62fe")
    })
  }

  runCode(value:string){
    this.errorOccured=false;
    this.loadingOutput=true;
    this.runButtonDisable=true;
    let random=Math.floor((Math.random() * 100) + 1);
    this.uniquekey=random
    let filename=this.uniquekey+"_"+this.lastClicked+this.extensionMap.get(this.lastClicked);
    var file = new File([value], filename, {type: 'text/plain', lastModified: Date.now()});
    this.uploadSevice.fetchServerURL().then(res=>{
    let result:any=res
    let backendurl=result.SERVER_URL
    this.uploadSevice.uploadFile(file,this.uniquekey,backendurl).subscribe((res:any)=>{
      console.log(res)
      this.waitMsg="Fetching the results...Please wait"
    },
    (err:any)=>{
      this.loadingOutput=false;
      this.runButtonDisable=false;
      this.errorOccured=true;
    })
  })
    this.fetchData$=this.uploadSevice.getResults(this.uniquekey) 
  //call the get API
  this.refreshInterval$ .pipe(
   // This kills the request if the user closes the component 
   takeUntil(this.killTrigger),
   // switchMap cancels the last request, if no response have been received since last tick
   switchMap(() => this.fetchData$),
 ).subscribe(result => {
   this.statusText = result
   this.displayOutput=true
  this.waitMsg="Waiting for remote server..."
   if(this.statusText.message=='completed'){
     this.killTrigger.next()
      this.loadingOutput=false;
      this.displayOutput=true
      this.output=this.statusText.output;
   }
   console.log(this.statusText)
 },
 err=>{
   console.log(err)
  });
  }

  changeLanguageText(event:any){
    console.log(event.target.id)
    this.uploadSevice.readFile(event.target.id).subscribe((content:string)=>{
      this.data=content;
      // this.render.setValue(this.render.selectRootElement("#codearea",true),"")
      // this.render.setValue(this.render.selectRootElement("#code",true),this.data)
      console.log(this.data)
      this.render.removeStyle(this.render.selectRootElement("#"+this.lastClicked,true),"border-bottom")
      this.render.setStyle(this.render.selectRootElement("#"+event.target.id,true),"border-bottom","2px solid #0f62fe")
      this.lastClicked=event.target.id;
    })
    this.runButtonDisable=false
    this.killTrigger.next()
    this.displayOutput=false
    this.errorOccured=false
    this.loadingOutput=false
    this.runButtonDisable=false
    }

    toggleTheme(){
      this.lightTheme= !this.lightTheme
      if(this.lightTheme==true){
        this.render.setStyle(this.render.selectRootElement("#custom-container",true),"background-color","#fff");
        this.render.setStyle(this.render.selectRootElement("#code",true),"color","black");
        this.render.setStyle(this.render.selectRootElement("#code",true),"font-weight","400");
        this.render.setStyle(this.render.selectRootElement("#themechange",true),"background-color","#fff");
        this.render.setStyle(this.render.selectRootElement("#themechange",true),"color","black");
        this.allowedLanguages.forEach(lan=>{
          this.render.setStyle(this.render.selectRootElement("#"+lan,true),"background-color","#fff");
          this.render.setStyle(this.render.selectRootElement("#"+lan,true),"color","black");
        });
        this.render.setStyle(this.render.selectRootElement("#blank-cont",true),"background-color","#fff");


      }
      else{
        this.render.removeStyle(this.render.selectRootElement("#custom-container",true),"background-color");
        this.render.removeStyle(this.render.selectRootElement("#code",true),"color");
        this.render.removeStyle(this.render.selectRootElement("#code",true),"font-weight");
        this.render.removeStyle(this.render.selectRootElement("#themechange",true),"background-color");
        this.render.removeStyle(this.render.selectRootElement("#themechange",true),"color");
        this.allowedLanguages.forEach(lan=>{
          this.render.removeStyle(this.render.selectRootElement("#"+lan,true),"background-color");
          this.render.removeStyle(this.render.selectRootElement("#"+lan,true),"color");
        });
        this.render.removeStyle(this.render.selectRootElement("#blank-cont",true),"background-color");

      }
    }

}
