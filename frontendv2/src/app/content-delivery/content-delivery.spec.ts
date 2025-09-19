import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContentDelivery } from './content-delivery';

describe('ContentDelivery', () => {
  let component: ContentDelivery;
  let fixture: ComponentFixture<ContentDelivery>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ContentDelivery]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ContentDelivery);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
