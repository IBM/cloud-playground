import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders ,HttpParams} from '@angular/common/http';
import { Observable,EMPTY } from "rxjs"
import { map } from 'rxjs/internal/operators/map';

class result{
  elapsed_time: string=""
  etc: string=""
  message: string=""
  output: string=""
  constructor(elapsed_time:string,etc:string,message:string,output:string) {
    this.elapsed_time=elapsed_time
    this.etc=etc
    this.message=message
    this.output=output
  }
}

@Injectable({
  providedIn: 'root'
})
export class FileuploadService {
  private backendurlConstant:string=""


  constructor(private http: HttpClient) { }

  readFile(lang:string){
    return this.http.get("assets/"+lang,{responseType: 'text'})
  }
  
  uploadFile(code:File,uniquekey:any,backendurl:string){
  let headers = new HttpHeaders({
    'Access-Control-Allow-Origin':'*' }
    );
  let options = { headers: headers };
    const formData = new FormData();
    formData.append("file",code)
    formData.append("id",uniquekey)
    return this.http.post(backendurl+"/code",formData,options)
  }

  getResults(uniqueId:any):Observable<result>{
    let result:Observable<result>=EMPTY
    this.fetchServerURL().then((res:any)=>{   
    this.backendurlConstant=res.SERVER_URL
    })
    if(this.backendurlConstant){
    let headers = new HttpHeaders({
      'Access-Control-Allow-Origin':'*' }
    );
  let params = new HttpParams(); 
    let options = { headers: headers , params :params.append('id', uniqueId) };
    return this.http.get<result>(this.backendurlConstant+"/result",options).pipe(
      map(response=>response)
    )
    }
    return result
  }

  
  async fetchServerURL() {
    return await this.http.get( 'assets/json/runtime.json' ).toPromise()  
   
  }
  
  getprivateKey():string{
    let privatekey:string=""
    this.http.get('assets/json/runtime.json' ).subscribe( 
        res => {
          let result:any=res
            privatekey=result.PRIVATE_KEY
        }
    );
    return privatekey
  }

  getpublickey(){
    let publickey:string=""
    this.http.get('assets/json/runtime.json').subscribe( 
        res => {
          let result:any=res
            publickey=result.PUBLIC_KEY
        }
    );
    return publickey

  }

}
