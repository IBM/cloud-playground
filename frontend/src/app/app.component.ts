import { Component } from '@angular/core';
import { FileuploadService } from './fileupload.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
 public data:string='';

  constructor(private uploadSevice: FileuploadService) { }

  ngOnInit(){
  
  } 

}