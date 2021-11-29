import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { FileuploadService } from './fileupload.service';
import { HeaderComponent } from './header/header.component';
import { CodeComponent } from './code/code.component';



@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    CodeComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FontAwesomeModule
  

  ],
  providers: [
    FileuploadService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
