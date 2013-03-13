from django.db.models import Q

from .models import Parcel


def find_parcel(address=None, centroid=None, mapreg=None):
    """Find a parcel."""
    filters = Q()

    # Try optimistic, fast query--assumes everything present will match
    if centroid:
        filters = filters & Q(geometry__contains=centroid)
    if address:
        filters = filters & (Q(address__iexact=address) |
                             Q(address__icontains=address))
    if mapreg:
        filters = filters & Q(mapreg=mapreg)

    parcels = Parcel.objects.filter(filters)
    if parcels.count() == 1:
        return parcels[0]

    # Optimistic failed, try each filter individually
    parcels = Parcel.objects.all()
    if address:
        print 'Trying to filter by address: "%s"' % address
        parcels = parcels.filter(address__iexact=address)
        if parcels.count() == 1:
            print '  ...success!'
            return parcels[0]
        if parcels.count() > 1:
            print ('Found too many parcels (%d) for address %s'
                   % (parcels.count(), address))
        else:
            parcels = Parcel.objects.all()

        print 'Trying to filter more loosely by address: "%s"' % address
        parcels = parcels.filter(address__icontains=address)
        if parcels.count() == 1:
            print '  ...success!'
            return parcels[0]
        if parcels.count() > 1:
            print ('Found too many parcels (%d) searching loosely for address %s'
                   % (parcels.count(), address))

    # filter by mapreg
    if mapreg:
        print 'Trying to filter by mapreg: "%s"' % mapreg
        parcels = parcels.filter(mapreg=mapreg)
        if parcels.count() == 1:
            print '  ...success!'
            return parcels[0]
        if parcels.count() > 1:
            print ('Found too many parcels (%d) for mapreg %s'
                   % (parcels.count(), mapreg))
        else:
            parcels = Parcel.objects.all()

    # filter by centroid
    if centroid:
        parcels = parcels.filter(geometry__contains=centroid)
        if parcels.count() == 1:
            return parcels[0]
        if parcels.count() > 1:
            print ('Found too many parcels (%d) for centroid %s'
                   % (parcels.count(), str(centroid)))
        else:
            parcels = Parcel.objects.all()

    if parcels.count() > 1:
        print 'Still too many parcels:'
        if parcels.count() < 5:
            for parcel in parcels:
                print '\tparcel:', parcel
        else:
            print '\t(too many to list)'
    return None
