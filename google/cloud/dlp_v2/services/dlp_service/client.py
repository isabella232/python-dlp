# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from collections import OrderedDict
import os
import re
from typing import Callable, Dict, Sequence, Tuple, Type, Union
import pkg_resources

import google.api_core.client_options as ClientOptions  # type: ignore
from google.api_core import exceptions  # type: ignore
from google.api_core import gapic_v1  # type: ignore
from google.api_core import retry as retries  # type: ignore
from google.auth import credentials  # type: ignore
from google.auth.transport import mtls  # type: ignore
from google.auth.exceptions import MutualTLSChannelError  # type: ignore
from google.oauth2 import service_account  # type: ignore

from google.cloud.dlp_v2.services.dlp_service import pagers
from google.cloud.dlp_v2.types import dlp
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import timestamp_pb2 as timestamp  # type: ignore

from .transports.base import DlpServiceTransport
from .transports.grpc import DlpServiceGrpcTransport
from .transports.grpc_asyncio import DlpServiceGrpcAsyncIOTransport


class DlpServiceClientMeta(type):
    """Metaclass for the DlpService client.

    This provides class-level methods for building and retrieving
    support objects (e.g. transport) without polluting the client instance
    objects.
    """

    _transport_registry = OrderedDict()  # type: Dict[str, Type[DlpServiceTransport]]
    _transport_registry["grpc"] = DlpServiceGrpcTransport
    _transport_registry["grpc_asyncio"] = DlpServiceGrpcAsyncIOTransport

    def get_transport_class(cls, label: str = None,) -> Type[DlpServiceTransport]:
        """Return an appropriate transport class.

        Args:
            label: The name of the desired transport. If none is
                provided, then the first transport in the registry is used.

        Returns:
            The transport class to use.
        """
        # If a specific transport is requested, return that one.
        if label:
            return cls._transport_registry[label]

        # No transport is requested; return the default (that is, the first one
        # in the dictionary).
        return next(iter(cls._transport_registry.values()))


class DlpServiceClient(metaclass=DlpServiceClientMeta):
    """The Cloud Data Loss Prevention (DLP) API is a service that
    allows clients to detect the presence of Personally Identifiable
    Information (PII) and other privacy-sensitive data in user-
    supplied, unstructured data streams, like text blocks or images.
    The service also includes methods for sensitive data redaction
    and scheduling of data scans on Google Cloud Platform based data
    sets.
    To learn more about concepts and find how-to guides see
    https://cloud.google.com/dlp/docs/.
    """

    @staticmethod
    def _get_default_mtls_endpoint(api_endpoint):
        """Convert api endpoint to mTLS endpoint.
        Convert "*.sandbox.googleapis.com" and "*.googleapis.com" to
        "*.mtls.sandbox.googleapis.com" and "*.mtls.googleapis.com" respectively.
        Args:
            api_endpoint (Optional[str]): the api endpoint to convert.
        Returns:
            str: converted mTLS api endpoint.
        """
        if not api_endpoint:
            return api_endpoint

        mtls_endpoint_re = re.compile(
            r"(?P<name>[^.]+)(?P<mtls>\.mtls)?(?P<sandbox>\.sandbox)?(?P<googledomain>\.googleapis\.com)?"
        )

        m = mtls_endpoint_re.match(api_endpoint)
        name, mtls, sandbox, googledomain = m.groups()
        if mtls or not googledomain:
            return api_endpoint

        if sandbox:
            return api_endpoint.replace(
                "sandbox.googleapis.com", "mtls.sandbox.googleapis.com"
            )

        return api_endpoint.replace(".googleapis.com", ".mtls.googleapis.com")

    DEFAULT_ENDPOINT = "dlp.googleapis.com"
    DEFAULT_MTLS_ENDPOINT = _get_default_mtls_endpoint.__func__(  # type: ignore
        DEFAULT_ENDPOINT
    )

    @classmethod
    def from_service_account_file(cls, filename: str, *args, **kwargs):
        """Creates an instance of this client using the provided credentials
        file.

        Args:
            filename (str): The path to the service account private key json
                file.
            args: Additional arguments to pass to the constructor.
            kwargs: Additional arguments to pass to the constructor.

        Returns:
            {@api.name}: The constructed client.
        """
        credentials = service_account.Credentials.from_service_account_file(filename)
        kwargs["credentials"] = credentials
        return cls(*args, **kwargs)

    from_service_account_json = from_service_account_file

    @staticmethod
    def deidentify_template_path(organization: str, deidentify_template: str,) -> str:
        """Return a fully-qualified deidentify_template string."""
        return "organizations/{organization}/deidentifyTemplates/{deidentify_template}".format(
            organization=organization, deidentify_template=deidentify_template,
        )

    @staticmethod
    def parse_deidentify_template_path(path: str) -> Dict[str, str]:
        """Parse a deidentify_template path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/deidentifyTemplates/(?P<deidentify_template>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def inspect_template_path(organization: str, inspect_template: str,) -> str:
        """Return a fully-qualified inspect_template string."""
        return "organizations/{organization}/inspectTemplates/{inspect_template}".format(
            organization=organization, inspect_template=inspect_template,
        )

    @staticmethod
    def parse_inspect_template_path(path: str) -> Dict[str, str]:
        """Parse a inspect_template path into its component segments."""
        m = re.match(
            r"^organizations/(?P<organization>.+?)/inspectTemplates/(?P<inspect_template>.+?)$",
            path,
        )
        return m.groupdict() if m else {}

    @staticmethod
    def job_trigger_path(project: str, job_trigger: str,) -> str:
        """Return a fully-qualified job_trigger string."""
        return "projects/{project}/jobTriggers/{job_trigger}".format(
            project=project, job_trigger=job_trigger,
        )

    @staticmethod
    def parse_job_trigger_path(path: str) -> Dict[str, str]:
        """Parse a job_trigger path into its component segments."""
        m = re.match(
            r"^projects/(?P<project>.+?)/jobTriggers/(?P<job_trigger>.+?)$", path
        )
        return m.groupdict() if m else {}

    def __init__(
        self,
        *,
        credentials: credentials.Credentials = None,
        transport: Union[str, DlpServiceTransport] = None,
        client_options: ClientOptions = None,
    ) -> None:
        """Instantiate the dlp service client.

        Args:
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
            transport (Union[str, ~.DlpServiceTransport]): The
                transport to use. If set to None, a transport is chosen
                automatically.
            client_options (ClientOptions): Custom options for the client. It
                won't take effect if a ``transport`` instance is provided.
                (1) The ``api_endpoint`` property can be used to override the
                default endpoint provided by the client. GOOGLE_API_USE_MTLS
                environment variable can also be used to override the endpoint:
                "always" (always use the default mTLS endpoint), "never" (always
                use the default regular endpoint, this is the default value for
                the environment variable) and "auto" (auto switch to the default
                mTLS endpoint if client SSL credentials is present). However,
                the ``api_endpoint`` property takes precedence if provided.
                (2) The ``client_cert_source`` property is used to provide client
                SSL credentials for mutual TLS transport. If not provided, the
                default SSL credentials will be used if present.

        Raises:
            google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
                creation failed for any reason.
        """
        if isinstance(client_options, dict):
            client_options = ClientOptions.from_dict(client_options)
        if client_options is None:
            client_options = ClientOptions.ClientOptions()

        if client_options.api_endpoint is None:
            use_mtls_env = os.getenv("GOOGLE_API_USE_MTLS", "never")
            if use_mtls_env == "never":
                client_options.api_endpoint = self.DEFAULT_ENDPOINT
            elif use_mtls_env == "always":
                client_options.api_endpoint = self.DEFAULT_MTLS_ENDPOINT
            elif use_mtls_env == "auto":
                has_client_cert_source = (
                    client_options.client_cert_source is not None
                    or mtls.has_default_client_cert_source()
                )
                client_options.api_endpoint = (
                    self.DEFAULT_MTLS_ENDPOINT
                    if has_client_cert_source
                    else self.DEFAULT_ENDPOINT
                )
            else:
                raise MutualTLSChannelError(
                    "Unsupported GOOGLE_API_USE_MTLS value. Accepted values: never, auto, always"
                )

        # Save or instantiate the transport.
        # Ordinarily, we provide the transport, but allowing a custom transport
        # instance provides an extensibility point for unusual situations.
        if isinstance(transport, DlpServiceTransport):
            # transport is a DlpServiceTransport instance.
            if credentials or client_options.credentials_file:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its credentials directly."
                )
            if client_options.scopes:
                raise ValueError(
                    "When providing a transport instance, "
                    "provide its scopes directly."
                )
            self._transport = transport
        else:
            Transport = type(self).get_transport_class(transport)
            self._transport = Transport(
                credentials=credentials,
                credentials_file=client_options.credentials_file,
                host=client_options.api_endpoint,
                scopes=client_options.scopes,
                api_mtls_endpoint=client_options.api_endpoint,
                client_cert_source=client_options.client_cert_source,
                quota_project_id=client_options.quota_project_id,
            )

    def inspect_content(
        self,
        request: dlp.InspectContentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.InspectContentResponse:
        r"""Finds potentially sensitive info in content.
        This method has limits on input size, processing time,
        and output size.
        When no InfoTypes or CustomInfoTypes are specified in
        this request, the system will automatically choose what
        detectors to run. By default this may be all types, but
        may change over time as detectors are updated.
        For how to guides, see
        https://cloud.google.com/dlp/docs/inspecting-images and
        https://cloud.google.com/dlp/docs/inspecting-text,

        Args:
            request (:class:`~.dlp.InspectContentRequest`):
                The request object. Request to search for potentially
                sensitive info in a ContentItem.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.InspectContentResponse:
                Results of inspecting an item.
        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.InspectContentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.InspectContentRequest):
            request = dlp.InspectContentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.inspect_content]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def redact_image(
        self,
        request: dlp.RedactImageRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.RedactImageResponse:
        r"""Redacts potentially sensitive info from an image.
        This method has limits on input size, processing time,
        and output size. See
        https://cloud.google.com/dlp/docs/redacting-sensitive-
        data-images to learn more.

        When no InfoTypes or CustomInfoTypes are specified in
        this request, the system will automatically choose what
        detectors to run. By default this may be all types, but
        may change over time as detectors are updated.

        Args:
            request (:class:`~.dlp.RedactImageRequest`):
                The request object. Request to search for potentially
                sensitive info in an image and redact it by covering it
                with a colored rectangle.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.RedactImageResponse:
                Results of redacting an image.
        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.RedactImageRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.RedactImageRequest):
            request = dlp.RedactImageRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.redact_image]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def deidentify_content(
        self,
        request: dlp.DeidentifyContentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DeidentifyContentResponse:
        r"""De-identifies potentially sensitive info from a
        ContentItem. This method has limits on input size and
        output size. See
        https://cloud.google.com/dlp/docs/deidentify-sensitive-
        data to learn more.

        When no InfoTypes or CustomInfoTypes are specified in
        this request, the system will automatically choose what
        detectors to run. By default this may be all types, but
        may change over time as detectors are updated.

        Args:
            request (:class:`~.dlp.DeidentifyContentRequest`):
                The request object. Request to de-identify a list of
                items.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.DeidentifyContentResponse:
                Results of de-identifying a
                ContentItem.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.DeidentifyContentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.DeidentifyContentRequest):
            request = dlp.DeidentifyContentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.deidentify_content]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def reidentify_content(
        self,
        request: dlp.ReidentifyContentRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.ReidentifyContentResponse:
        r"""Re-identifies content that has been de-identified. See
        https://cloud.google.com/dlp/docs/pseudonymization#re-identification_in_free_text_code_example
        to learn more.

        Args:
            request (:class:`~.dlp.ReidentifyContentRequest`):
                The request object. Request to re-identify an item.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.ReidentifyContentResponse:
                Results of re-identifying a item.
        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ReidentifyContentRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ReidentifyContentRequest):
            request = dlp.ReidentifyContentRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.reidentify_content]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_info_types(
        self,
        request: dlp.ListInfoTypesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.ListInfoTypesResponse:
        r"""Returns a list of the sensitive information types
        that the DLP API supports. See
        https://cloud.google.com/dlp/docs/infotypes-reference to
        learn more.

        Args:
            request (:class:`~.dlp.ListInfoTypesRequest`):
                The request object. Request for the list of infoTypes.
            parent (:class:`str`):
                The parent resource name.

                -  Format:locations/[LOCATION-ID]
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.ListInfoTypesResponse:
                Response to the ListInfoTypes
                request.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ListInfoTypesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ListInfoTypesRequest):
            request = dlp.ListInfoTypesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_info_types]

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_inspect_template(
        self,
        request: dlp.CreateInspectTemplateRequest = None,
        *,
        parent: str = None,
        inspect_template: dlp.InspectTemplate = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.InspectTemplate:
        r"""Creates an InspectTemplate for re-using frequently
        used configuration for inspecting content, images, and
        storage. See https://cloud.google.com/dlp/docs/creating-
        templates to learn more.

        Args:
            request (:class:`~.dlp.CreateInspectTemplateRequest`):
                The request object. Request message for
                CreateInspectTemplate.
            parent (:class:`str`):
                Required. Parent resource name.

                -  Format:projects/[PROJECT-ID]
                -  Format:organizations/[ORGANIZATION-ID]
                -  Format:projects/[PROJECT-ID]/locations/[LOCATION-ID]
                -  Format:organizations/[ORGANIZATION-ID]/locations/[LOCATION-ID]
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            inspect_template (:class:`~.dlp.InspectTemplate`):
                Required. The InspectTemplate to
                create.
                This corresponds to the ``inspect_template`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.InspectTemplate:
                The inspectTemplate contains a
                configuration (set of types of sensitive
                data to be detected) to be used anywhere
                you otherwise would normally specify
                InspectConfig. See
                https://cloud.google.com/dlp/docs/concepts-
                templates to learn more.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, inspect_template])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.CreateInspectTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.CreateInspectTemplateRequest):
            request = dlp.CreateInspectTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if inspect_template is not None:
                request.inspect_template = inspect_template

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_inspect_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_inspect_template(
        self,
        request: dlp.UpdateInspectTemplateRequest = None,
        *,
        name: str = None,
        inspect_template: dlp.InspectTemplate = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.InspectTemplate:
        r"""Updates the InspectTemplate.
        See https://cloud.google.com/dlp/docs/creating-templates
        to learn more.

        Args:
            request (:class:`~.dlp.UpdateInspectTemplateRequest`):
                The request object. Request message for
                UpdateInspectTemplate.
            name (:class:`str`):
                Required. Resource name of organization and
                inspectTemplate to be updated, for example
                ``organizations/433245324/inspectTemplates/432452342``
                or projects/project-id/inspectTemplates/432452342.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            inspect_template (:class:`~.dlp.InspectTemplate`):
                New InspectTemplate value.
                This corresponds to the ``inspect_template`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                Mask to control which fields get
                updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.InspectTemplate:
                The inspectTemplate contains a
                configuration (set of types of sensitive
                data to be detected) to be used anywhere
                you otherwise would normally specify
                InspectConfig. See
                https://cloud.google.com/dlp/docs/concepts-
                templates to learn more.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, inspect_template, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.UpdateInspectTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.UpdateInspectTemplateRequest):
            request = dlp.UpdateInspectTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name
            if inspect_template is not None:
                request.inspect_template = inspect_template
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_inspect_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_inspect_template(
        self,
        request: dlp.GetInspectTemplateRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.InspectTemplate:
        r"""Gets an InspectTemplate.
        See https://cloud.google.com/dlp/docs/creating-templates
        to learn more.

        Args:
            request (:class:`~.dlp.GetInspectTemplateRequest`):
                The request object. Request message for
                GetInspectTemplate.
            name (:class:`str`):
                Required. Resource name of the organization and
                inspectTemplate to be read, for example
                ``organizations/433245324/inspectTemplates/432452342``
                or projects/project-id/inspectTemplates/432452342.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.InspectTemplate:
                The inspectTemplate contains a
                configuration (set of types of sensitive
                data to be detected) to be used anywhere
                you otherwise would normally specify
                InspectConfig. See
                https://cloud.google.com/dlp/docs/concepts-
                templates to learn more.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.GetInspectTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.GetInspectTemplateRequest):
            request = dlp.GetInspectTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_inspect_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_inspect_templates(
        self,
        request: dlp.ListInspectTemplatesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListInspectTemplatesPager:
        r"""Lists InspectTemplates.
        See https://cloud.google.com/dlp/docs/creating-templates
        to learn more.

        Args:
            request (:class:`~.dlp.ListInspectTemplatesRequest`):
                The request object. Request message for
                ListInspectTemplates.
            parent (:class:`str`):
                Required. Parent resource name.

                -  Format:projects/[PROJECT-ID]
                -  Format:organizations/[ORGANIZATION-ID]
                -  Format:projects/[PROJECT-ID]/locations/[LOCATION-ID]
                -  Format:organizations/[ORGANIZATION-ID]/locations/[LOCATION-ID]
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListInspectTemplatesPager:
                Response message for
                ListInspectTemplates.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ListInspectTemplatesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ListInspectTemplatesRequest):
            request = dlp.ListInspectTemplatesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_inspect_templates]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListInspectTemplatesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_inspect_template(
        self,
        request: dlp.DeleteInspectTemplateRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes an InspectTemplate.
        See https://cloud.google.com/dlp/docs/creating-templates
        to learn more.

        Args:
            request (:class:`~.dlp.DeleteInspectTemplateRequest`):
                The request object. Request message for
                DeleteInspectTemplate.
            name (:class:`str`):
                Required. Resource name of the organization and
                inspectTemplate to be deleted, for example
                ``organizations/433245324/inspectTemplates/432452342``
                or projects/project-id/inspectTemplates/432452342.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.DeleteInspectTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.DeleteInspectTemplateRequest):
            request = dlp.DeleteInspectTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_inspect_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def create_deidentify_template(
        self,
        request: dlp.CreateDeidentifyTemplateRequest = None,
        *,
        parent: str = None,
        deidentify_template: dlp.DeidentifyTemplate = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DeidentifyTemplate:
        r"""Creates a DeidentifyTemplate for re-using frequently
        used configuration for de-identifying content, images,
        and storage. See
        https://cloud.google.com/dlp/docs/creating-templates-
        deid to learn more.

        Args:
            request (:class:`~.dlp.CreateDeidentifyTemplateRequest`):
                The request object. Request message for
                CreateDeidentifyTemplate.
            parent (:class:`str`):
                Required. Parent resource name.

                -  Format:projects/[PROJECT-ID]
                -  Format:organizations/[ORGANIZATION-ID]
                -  Format:projects/[PROJECT-ID]/locations/[LOCATION-ID]
                -  Format:organizations/[ORGANIZATION-ID]/locations/[LOCATION-ID]
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            deidentify_template (:class:`~.dlp.DeidentifyTemplate`):
                Required. The DeidentifyTemplate to
                create.
                This corresponds to the ``deidentify_template`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.DeidentifyTemplate:
                DeidentifyTemplates contains
                instructions on how to de-identify
                content. See
                https://cloud.google.com/dlp/docs/concepts-
                templates to learn more.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, deidentify_template])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.CreateDeidentifyTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.CreateDeidentifyTemplateRequest):
            request = dlp.CreateDeidentifyTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if deidentify_template is not None:
                request.deidentify_template = deidentify_template

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.create_deidentify_template
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_deidentify_template(
        self,
        request: dlp.UpdateDeidentifyTemplateRequest = None,
        *,
        name: str = None,
        deidentify_template: dlp.DeidentifyTemplate = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DeidentifyTemplate:
        r"""Updates the DeidentifyTemplate.
        See https://cloud.google.com/dlp/docs/creating-
        templates-deid to learn more.

        Args:
            request (:class:`~.dlp.UpdateDeidentifyTemplateRequest`):
                The request object. Request message for
                UpdateDeidentifyTemplate.
            name (:class:`str`):
                Required. Resource name of organization and deidentify
                template to be updated, for example
                ``organizations/433245324/deidentifyTemplates/432452342``
                or projects/project-id/deidentifyTemplates/432452342.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            deidentify_template (:class:`~.dlp.DeidentifyTemplate`):
                New DeidentifyTemplate value.
                This corresponds to the ``deidentify_template`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                Mask to control which fields get
                updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.DeidentifyTemplate:
                DeidentifyTemplates contains
                instructions on how to de-identify
                content. See
                https://cloud.google.com/dlp/docs/concepts-
                templates to learn more.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, deidentify_template, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.UpdateDeidentifyTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.UpdateDeidentifyTemplateRequest):
            request = dlp.UpdateDeidentifyTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name
            if deidentify_template is not None:
                request.deidentify_template = deidentify_template
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.update_deidentify_template
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_deidentify_template(
        self,
        request: dlp.GetDeidentifyTemplateRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DeidentifyTemplate:
        r"""Gets a DeidentifyTemplate.
        See https://cloud.google.com/dlp/docs/creating-
        templates-deid to learn more.

        Args:
            request (:class:`~.dlp.GetDeidentifyTemplateRequest`):
                The request object. Request message for
                GetDeidentifyTemplate.
            name (:class:`str`):
                Required. Resource name of the organization and
                deidentify template to be read, for example
                ``organizations/433245324/deidentifyTemplates/432452342``
                or projects/project-id/deidentifyTemplates/432452342.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.DeidentifyTemplate:
                DeidentifyTemplates contains
                instructions on how to de-identify
                content. See
                https://cloud.google.com/dlp/docs/concepts-
                templates to learn more.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.GetDeidentifyTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.GetDeidentifyTemplateRequest):
            request = dlp.GetDeidentifyTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_deidentify_template]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_deidentify_templates(
        self,
        request: dlp.ListDeidentifyTemplatesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDeidentifyTemplatesPager:
        r"""Lists DeidentifyTemplates.
        See https://cloud.google.com/dlp/docs/creating-
        templates-deid to learn more.

        Args:
            request (:class:`~.dlp.ListDeidentifyTemplatesRequest`):
                The request object. Request message for
                ListDeidentifyTemplates.
            parent (:class:`str`):
                Required. Parent resource name.

                -  Format:projects/[PROJECT-ID]
                -  Format:organizations/[ORGANIZATION-ID]
                -  Format:projects/[PROJECT-ID]/locations/[LOCATION-ID]
                -  Format:organizations/[ORGANIZATION-ID]/locations/[LOCATION-ID]
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListDeidentifyTemplatesPager:
                Response message for
                ListDeidentifyTemplates.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ListDeidentifyTemplatesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ListDeidentifyTemplatesRequest):
            request = dlp.ListDeidentifyTemplatesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.list_deidentify_templates
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDeidentifyTemplatesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_deidentify_template(
        self,
        request: dlp.DeleteDeidentifyTemplateRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a DeidentifyTemplate.
        See https://cloud.google.com/dlp/docs/creating-
        templates-deid to learn more.

        Args:
            request (:class:`~.dlp.DeleteDeidentifyTemplateRequest`):
                The request object. Request message for
                DeleteDeidentifyTemplate.
            name (:class:`str`):
                Required. Resource name of the organization and
                deidentify template to be deleted, for example
                ``organizations/433245324/deidentifyTemplates/432452342``
                or projects/project-id/deidentifyTemplates/432452342.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.DeleteDeidentifyTemplateRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.DeleteDeidentifyTemplateRequest):
            request = dlp.DeleteDeidentifyTemplateRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.delete_deidentify_template
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def create_job_trigger(
        self,
        request: dlp.CreateJobTriggerRequest = None,
        *,
        parent: str = None,
        job_trigger: dlp.JobTrigger = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.JobTrigger:
        r"""Creates a job trigger to run DLP actions such as
        scanning storage for sensitive information on a set
        schedule. See
        https://cloud.google.com/dlp/docs/creating-job-triggers
        to learn more.

        Args:
            request (:class:`~.dlp.CreateJobTriggerRequest`):
                The request object. Request message for
                CreateJobTrigger.
            parent (:class:`str`):
                Required. Parent resource name.

                -  Format:projects/[PROJECT-ID]
                -  Format:projects/[PROJECT-ID]/locations/[LOCATION-ID]
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job_trigger (:class:`~.dlp.JobTrigger`):
                Required. The JobTrigger to create.
                This corresponds to the ``job_trigger`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.JobTrigger:
                Contains a configuration to make dlp
                api calls on a repeating basis. See
                https://cloud.google.com/dlp/docs/concepts-
                job-triggers to learn more.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, job_trigger])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.CreateJobTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.CreateJobTriggerRequest):
            request = dlp.CreateJobTriggerRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if job_trigger is not None:
                request.job_trigger = job_trigger

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_job_trigger]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_job_trigger(
        self,
        request: dlp.UpdateJobTriggerRequest = None,
        *,
        name: str = None,
        job_trigger: dlp.JobTrigger = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.JobTrigger:
        r"""Updates a job trigger.
        See https://cloud.google.com/dlp/docs/creating-job-
        triggers to learn more.

        Args:
            request (:class:`~.dlp.UpdateJobTriggerRequest`):
                The request object. Request message for
                UpdateJobTrigger.
            name (:class:`str`):
                Required. Resource name of the project and the
                triggeredJob, for example
                ``projects/dlp-test-project/jobTriggers/53234423``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            job_trigger (:class:`~.dlp.JobTrigger`):
                New JobTrigger value.
                This corresponds to the ``job_trigger`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                Mask to control which fields get
                updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.JobTrigger:
                Contains a configuration to make dlp
                api calls on a repeating basis. See
                https://cloud.google.com/dlp/docs/concepts-
                job-triggers to learn more.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, job_trigger, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.UpdateJobTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.UpdateJobTriggerRequest):
            request = dlp.UpdateJobTriggerRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name
            if job_trigger is not None:
                request.job_trigger = job_trigger
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_job_trigger]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def hybrid_inspect_job_trigger(
        self,
        request: dlp.HybridInspectJobTriggerRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.HybridInspectResponse:
        r"""Inspect hybrid content and store findings to a
        trigger. The inspection will be processed
        asynchronously. To review the findings monitor the jobs
        within the trigger.
        Early access feature is in a pre-release state and might
        change or have limited support. For more information,
        see
        https://cloud.google.com/products#product-launch-stages.

        Args:
            request (:class:`~.dlp.HybridInspectJobTriggerRequest`):
                The request object. Request to search for potentially
                sensitive info in a custom location.
            name (:class:`str`):
                Required. Resource name of the trigger to execute a
                hybrid inspect on, for example
                ``projects/dlp-test-project/jobTriggers/53234423``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.HybridInspectResponse:
                Quota exceeded errors will be thrown
                once quota has been met.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.HybridInspectJobTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.HybridInspectJobTriggerRequest):
            request = dlp.HybridInspectJobTriggerRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[
            self._transport.hybrid_inspect_job_trigger
        ]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_job_trigger(
        self,
        request: dlp.GetJobTriggerRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.JobTrigger:
        r"""Gets a job trigger.
        See https://cloud.google.com/dlp/docs/creating-job-
        triggers to learn more.

        Args:
            request (:class:`~.dlp.GetJobTriggerRequest`):
                The request object. Request message for GetJobTrigger.
            name (:class:`str`):
                Required. Resource name of the project and the
                triggeredJob, for example
                ``projects/dlp-test-project/jobTriggers/53234423``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.JobTrigger:
                Contains a configuration to make dlp
                api calls on a repeating basis. See
                https://cloud.google.com/dlp/docs/concepts-
                job-triggers to learn more.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.GetJobTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.GetJobTriggerRequest):
            request = dlp.GetJobTriggerRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_job_trigger]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_job_triggers(
        self,
        request: dlp.ListJobTriggersRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListJobTriggersPager:
        r"""Lists job triggers.
        See https://cloud.google.com/dlp/docs/creating-job-
        triggers to learn more.

        Args:
            request (:class:`~.dlp.ListJobTriggersRequest`):
                The request object. Request message for ListJobTriggers.
            parent (:class:`str`):
                Required. Parent resource name.

                -  Format:projects/[PROJECT-ID]
                -  Format:projects/[PROJECT-ID]/locations/[LOCATION-ID]
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListJobTriggersPager:
                Response message for ListJobTriggers.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ListJobTriggersRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ListJobTriggersRequest):
            request = dlp.ListJobTriggersRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_job_triggers]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListJobTriggersPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_job_trigger(
        self,
        request: dlp.DeleteJobTriggerRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a job trigger.
        See https://cloud.google.com/dlp/docs/creating-job-
        triggers to learn more.

        Args:
            request (:class:`~.dlp.DeleteJobTriggerRequest`):
                The request object. Request message for
                DeleteJobTrigger.
            name (:class:`str`):
                Required. Resource name of the project and the
                triggeredJob, for example
                ``projects/dlp-test-project/jobTriggers/53234423``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.DeleteJobTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.DeleteJobTriggerRequest):
            request = dlp.DeleteJobTriggerRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_job_trigger]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def activate_job_trigger(
        self,
        request: dlp.ActivateJobTriggerRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DlpJob:
        r"""Activate a job trigger. Causes the immediate execute
        of a trigger instead of waiting on the trigger event to
        occur.

        Args:
            request (:class:`~.dlp.ActivateJobTriggerRequest`):
                The request object. Request message for
                ActivateJobTrigger.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.DlpJob:
                Combines all of the information about
                a DLP job.

        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ActivateJobTriggerRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ActivateJobTriggerRequest):
            request = dlp.ActivateJobTriggerRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.activate_job_trigger]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def create_dlp_job(
        self,
        request: dlp.CreateDlpJobRequest = None,
        *,
        parent: str = None,
        inspect_job: dlp.InspectJobConfig = None,
        risk_job: dlp.RiskAnalysisJobConfig = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DlpJob:
        r"""Creates a new job to inspect storage or calculate
        risk metrics. See
        https://cloud.google.com/dlp/docs/inspecting-storage and
        https://cloud.google.com/dlp/docs/compute-risk-analysis
        to learn more.
        When no InfoTypes or CustomInfoTypes are specified in
        inspect jobs, the system will automatically choose what
        detectors to run. By default this may be all types, but
        may change over time as detectors are updated.

        Args:
            request (:class:`~.dlp.CreateDlpJobRequest`):
                The request object. Request message for
                CreateDlpJobRequest. Used to initiate long running jobs
                such as calculating risk metrics or inspecting Google
                Cloud Storage.
            parent (:class:`str`):
                Required. Parent resource name.

                -  Format:projects/[PROJECT-ID]
                -  Format:projects/[PROJECT-ID]/locations/[LOCATION-ID]
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            inspect_job (:class:`~.dlp.InspectJobConfig`):
                Set to control what and how to
                inspect.
                This corresponds to the ``inspect_job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            risk_job (:class:`~.dlp.RiskAnalysisJobConfig`):
                Set to choose what metric to
                calculate.
                This corresponds to the ``risk_job`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.DlpJob:
                Combines all of the information about
                a DLP job.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, inspect_job, risk_job])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.CreateDlpJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.CreateDlpJobRequest):
            request = dlp.CreateDlpJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if inspect_job is not None:
                request.inspect_job = inspect_job
            if risk_job is not None:
                request.risk_job = risk_job

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_dlp_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_dlp_jobs(
        self,
        request: dlp.ListDlpJobsRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListDlpJobsPager:
        r"""Lists DlpJobs that match the specified filter in the
        request. See
        https://cloud.google.com/dlp/docs/inspecting-storage and
        https://cloud.google.com/dlp/docs/compute-risk-analysis
        to learn more.

        Args:
            request (:class:`~.dlp.ListDlpJobsRequest`):
                The request object. The request message for listing DLP
                jobs.
            parent (:class:`str`):
                Required. Parent resource name.

                -  Format:projects/[PROJECT-ID]
                -  Format:projects/[PROJECT-ID]/locations/[LOCATION-ID]
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListDlpJobsPager:
                The response message for listing DLP
                jobs.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ListDlpJobsRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ListDlpJobsRequest):
            request = dlp.ListDlpJobsRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_dlp_jobs]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListDlpJobsPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def get_dlp_job(
        self,
        request: dlp.GetDlpJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.DlpJob:
        r"""Gets the latest state of a long-running DlpJob.
        See https://cloud.google.com/dlp/docs/inspecting-storage
        and https://cloud.google.com/dlp/docs/compute-risk-
        analysis to learn more.

        Args:
            request (:class:`~.dlp.GetDlpJobRequest`):
                The request object. The request message for
                [DlpJobs.GetDlpJob][].
            name (:class:`str`):
                Required. The name of the DlpJob
                resource.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.DlpJob:
                Combines all of the information about
                a DLP job.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.GetDlpJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.GetDlpJobRequest):
            request = dlp.GetDlpJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_dlp_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def delete_dlp_job(
        self,
        request: dlp.DeleteDlpJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a long-running DlpJob. This method indicates
        that the client is no longer interested in the DlpJob
        result. The job will be cancelled if possible.
        See https://cloud.google.com/dlp/docs/inspecting-storage
        and https://cloud.google.com/dlp/docs/compute-risk-
        analysis to learn more.

        Args:
            request (:class:`~.dlp.DeleteDlpJobRequest`):
                The request object. The request message for deleting a
                DLP job.
            name (:class:`str`):
                Required. The name of the DlpJob
                resource to be deleted.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.DeleteDlpJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.DeleteDlpJobRequest):
            request = dlp.DeleteDlpJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_dlp_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def cancel_dlp_job(
        self,
        request: dlp.CancelDlpJobRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Starts asynchronous cancellation on a long-running
        DlpJob. The server makes a best effort to cancel the
        DlpJob, but success is not guaranteed.
        See https://cloud.google.com/dlp/docs/inspecting-storage
        and https://cloud.google.com/dlp/docs/compute-risk-
        analysis to learn more.

        Args:
            request (:class:`~.dlp.CancelDlpJobRequest`):
                The request object. The request message for canceling a
                DLP job.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.CancelDlpJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.CancelDlpJobRequest):
            request = dlp.CancelDlpJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.cancel_dlp_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def create_stored_info_type(
        self,
        request: dlp.CreateStoredInfoTypeRequest = None,
        *,
        parent: str = None,
        config: dlp.StoredInfoTypeConfig = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.StoredInfoType:
        r"""Creates a pre-built stored infoType to be used for
        inspection. See
        https://cloud.google.com/dlp/docs/creating-stored-
        infotypes to learn more.

        Args:
            request (:class:`~.dlp.CreateStoredInfoTypeRequest`):
                The request object. Request message for
                CreateStoredInfoType.
            parent (:class:`str`):
                Required. Parent resource name.

                -  Format:projects/[PROJECT-ID]
                -  Format:organizations/[ORGANIZATION-ID]
                -  Format:projects/[PROJECT-ID]/locations/[LOCATION-ID]
                -  Format:organizations/[ORGANIZATION-ID]/locations/[LOCATION-ID]
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            config (:class:`~.dlp.StoredInfoTypeConfig`):
                Required. Configuration of the
                storedInfoType to create.
                This corresponds to the ``config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.StoredInfoType:
                StoredInfoType resource message that
                contains information about the current
                version and any pending updates.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent, config])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.CreateStoredInfoTypeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.CreateStoredInfoTypeRequest):
            request = dlp.CreateStoredInfoTypeRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent
            if config is not None:
                request.config = config

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.create_stored_info_type]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def update_stored_info_type(
        self,
        request: dlp.UpdateStoredInfoTypeRequest = None,
        *,
        name: str = None,
        config: dlp.StoredInfoTypeConfig = None,
        update_mask: field_mask.FieldMask = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.StoredInfoType:
        r"""Updates the stored infoType by creating a new
        version. The existing version will continue to be used
        until the new version is ready. See
        https://cloud.google.com/dlp/docs/creating-stored-
        infotypes to learn more.

        Args:
            request (:class:`~.dlp.UpdateStoredInfoTypeRequest`):
                The request object. Request message for
                UpdateStoredInfoType.
            name (:class:`str`):
                Required. Resource name of organization and
                storedInfoType to be updated, for example
                ``organizations/433245324/storedInfoTypes/432452342`` or
                projects/project-id/storedInfoTypes/432452342.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            config (:class:`~.dlp.StoredInfoTypeConfig`):
                Updated configuration for the
                storedInfoType. If not provided, a new
                version of the storedInfoType will be
                created with the existing configuration.
                This corresponds to the ``config`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.
            update_mask (:class:`~.field_mask.FieldMask`):
                Mask to control which fields get
                updated.
                This corresponds to the ``update_mask`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.StoredInfoType:
                StoredInfoType resource message that
                contains information about the current
                version and any pending updates.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name, config, update_mask])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.UpdateStoredInfoTypeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.UpdateStoredInfoTypeRequest):
            request = dlp.UpdateStoredInfoTypeRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name
            if config is not None:
                request.config = config
            if update_mask is not None:
                request.update_mask = update_mask

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.update_stored_info_type]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def get_stored_info_type(
        self,
        request: dlp.GetStoredInfoTypeRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.StoredInfoType:
        r"""Gets a stored infoType.
        See https://cloud.google.com/dlp/docs/creating-stored-
        infotypes to learn more.

        Args:
            request (:class:`~.dlp.GetStoredInfoTypeRequest`):
                The request object. Request message for
                GetStoredInfoType.
            name (:class:`str`):
                Required. Resource name of the organization and
                storedInfoType to be read, for example
                ``organizations/433245324/storedInfoTypes/432452342`` or
                projects/project-id/storedInfoTypes/432452342.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.StoredInfoType:
                StoredInfoType resource message that
                contains information about the current
                version and any pending updates.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.GetStoredInfoTypeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.GetStoredInfoTypeRequest):
            request = dlp.GetStoredInfoTypeRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.get_stored_info_type]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def list_stored_info_types(
        self,
        request: dlp.ListStoredInfoTypesRequest = None,
        *,
        parent: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> pagers.ListStoredInfoTypesPager:
        r"""Lists stored infoTypes.
        See https://cloud.google.com/dlp/docs/creating-stored-
        infotypes to learn more.

        Args:
            request (:class:`~.dlp.ListStoredInfoTypesRequest`):
                The request object. Request message for
                ListStoredInfoTypes.
            parent (:class:`str`):
                Required. Parent resource name.

                -  Format:projects/[PROJECT-ID]
                -  Format:organizations/[ORGANIZATION-ID]
                -  Format:projects/[PROJECT-ID]/locations/[LOCATION-ID]
                -  Format:organizations/[ORGANIZATION-ID]/locations/[LOCATION-ID]
                This corresponds to the ``parent`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.pagers.ListStoredInfoTypesPager:
                Response message for
                ListStoredInfoTypes.
                Iterating over this object will yield
                results and resolve additional pages
                automatically.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([parent])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.ListStoredInfoTypesRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.ListStoredInfoTypesRequest):
            request = dlp.ListStoredInfoTypesRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if parent is not None:
                request.parent = parent

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.list_stored_info_types]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("parent", request.parent),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # This method is paged; wrap the response in a pager, which provides
        # an `__iter__` convenience method.
        response = pagers.ListStoredInfoTypesPager(
            method=rpc, request=request, response=response, metadata=metadata,
        )

        # Done; return the response.
        return response

    def delete_stored_info_type(
        self,
        request: dlp.DeleteStoredInfoTypeRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Deletes a stored infoType.
        See https://cloud.google.com/dlp/docs/creating-stored-
        infotypes to learn more.

        Args:
            request (:class:`~.dlp.DeleteStoredInfoTypeRequest`):
                The request object. Request message for
                DeleteStoredInfoType.
            name (:class:`str`):
                Required. Resource name of the organization and
                storedInfoType to be deleted, for example
                ``organizations/433245324/storedInfoTypes/432452342`` or
                projects/project-id/storedInfoTypes/432452342.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.DeleteStoredInfoTypeRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.DeleteStoredInfoTypeRequest):
            request = dlp.DeleteStoredInfoTypeRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.delete_stored_info_type]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )

    def hybrid_inspect_dlp_job(
        self,
        request: dlp.HybridInspectDlpJobRequest = None,
        *,
        name: str = None,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> dlp.HybridInspectResponse:
        r"""Inspect hybrid content and store findings to a job.
        To review the findings inspect the job. Inspection will
        occur asynchronously.
        Early access feature is in a pre-release state and might
        change or have limited support. For more information,
        see
        https://cloud.google.com/products#product-launch-stages.

        Args:
            request (:class:`~.dlp.HybridInspectDlpJobRequest`):
                The request object. Request to search for potentially
                sensitive info in a custom location.
            name (:class:`str`):
                Required. Resource name of the job to execute a hybrid
                inspect on, for example
                ``projects/dlp-test-project/dlpJob/53234423``.
                This corresponds to the ``name`` field
                on the ``request`` instance; if ``request`` is provided, this
                should not be set.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.

        Returns:
            ~.dlp.HybridInspectResponse:
                Quota exceeded errors will be thrown
                once quota has been met.

        """
        # Create or coerce a protobuf request object.
        # Sanity check: If we got a request object, we should *not* have
        # gotten any keyword arguments that map to the request.
        has_flattened_params = any([name])
        if request is not None and has_flattened_params:
            raise ValueError(
                "If the `request` argument is set, then none of "
                "the individual field arguments should be set."
            )

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.HybridInspectDlpJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.HybridInspectDlpJobRequest):
            request = dlp.HybridInspectDlpJobRequest(request)

            # If we have keyword arguments corresponding to fields on the
            # request, apply these.

            if name is not None:
                request.name = name

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.hybrid_inspect_dlp_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        response = rpc(request, retry=retry, timeout=timeout, metadata=metadata,)

        # Done; return the response.
        return response

    def finish_dlp_job(
        self,
        request: dlp.FinishDlpJobRequest = None,
        *,
        retry: retries.Retry = gapic_v1.method.DEFAULT,
        timeout: float = None,
        metadata: Sequence[Tuple[str, str]] = (),
    ) -> None:
        r"""Finish a running hybrid DlpJob. Triggers the
        finalization steps and running of any enabled actions
        that have not yet run. Early access feature is in a pre-
        release state and might change or have limited support.
        For more information, see
        https://cloud.google.com/products#product-launch-stages.

        Args:
            request (:class:`~.dlp.FinishDlpJobRequest`):
                The request object. The request message for finishing a
                DLP hybrid job.

            retry (google.api_core.retry.Retry): Designation of what errors, if any,
                should be retried.
            timeout (float): The timeout for this request.
            metadata (Sequence[Tuple[str, str]]): Strings which should be
                sent along with the request as metadata.
        """
        # Create or coerce a protobuf request object.

        # Minor optimization to avoid making a copy if the user passes
        # in a dlp.FinishDlpJobRequest.
        # There's no risk of modifying the input as we've already verified
        # there are no flattened fields.
        if not isinstance(request, dlp.FinishDlpJobRequest):
            request = dlp.FinishDlpJobRequest(request)

        # Wrap the RPC method; this adds retry and timeout information,
        # and friendly error handling.
        rpc = self._transport._wrapped_methods[self._transport.finish_dlp_job]

        # Certain fields should be provided within the metadata header;
        # add these here.
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((("name", request.name),)),
        )

        # Send the request.
        rpc(
            request, retry=retry, timeout=timeout, metadata=metadata,
        )


try:
    _client_info = gapic_v1.client_info.ClientInfo(
        gapic_version=pkg_resources.get_distribution("google-cloud-dlp",).version,
    )
except pkg_resources.DistributionNotFound:
    _client_info = gapic_v1.client_info.ClientInfo()


__all__ = ("DlpServiceClient",)
