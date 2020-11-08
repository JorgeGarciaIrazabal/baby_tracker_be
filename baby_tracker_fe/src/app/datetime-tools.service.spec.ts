import { TestBed } from '@angular/core/testing';

import { DatetimeToolsService } from './datetime-tools.service';

describe('DatetimeToolsService', () => {
  let service: DatetimeToolsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DatetimeToolsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
