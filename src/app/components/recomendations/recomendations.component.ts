import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ElectronService } from '../../providers/electron.service';

@Component({
  selector: 'app-recomendations',
  templateUrl: './recomendations.component.html',
  styleUrls: ['./recomendations.component.css']
})
export class RecomendationsComponent implements OnInit {
  encryptedCapsule: any;
  rekey: any;
  constructor(private http: HttpClient, private electronService: ElectronService) { }

  ngOnInit() {
  }

  getCapsuleFromServer(){
    return this.http.post<any>(
      'https://nuserver.appspot.com/generate_key_pair', {})
    .subscribe((data: any) => {
      this.encryptedCapsule = data.encrypted_result;
      this.sendToPythonEncrypdedCapsule('@@@Public Key');
    })
  }

  sendToPythonEncrypdedCapsule(capsule: string) {
    this.electronService.ipcRenderer.send('asynchronous-message', capsule);
    this.electronService.ipcRenderer.on('asynchronous-reply', (event, arg) => {
      this.rekey = arg;
      console.log('this.rekey :', this.rekey);
    })        
  }
}
