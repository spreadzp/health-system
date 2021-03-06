import { HomeComponent } from './components/home/home.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RecomendationsComponent } from './components/recomendations/recomendations.component';
import { ReportsComponent } from './components/reports/reports.component';
import { SensorsComponent } from './components/sensors/sensors.component';
import { DocBoardComponent } from './components/doc-board/doc-board.component';
import { MetaSenderComponent } from './components/meta/meta-sender/meta-sender.component';

const routes: Routes = [
    { path: '', redirectTo: '/meta', pathMatch: 'full' },
    { path: 'meta', component: MetaSenderComponent },
    { path: 'recomdations', component: RecomendationsComponent },
    { path: 'reports', component: ReportsComponent },
    { path: 'sensors', component: SensorsComponent },
    { path: 'doc-board', component: DocBoardComponent },
    { path: '**', redirectTo: '/meta'}
  
  ];

@NgModule({
    imports: [RouterModule.forRoot(routes, {useHash: true})],
    exports: [RouterModule]
})
export class AppRoutingModule { }
